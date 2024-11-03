from sqlalchemy import text
from django.conf import settings
from report.models import Report
from core.db_manager import DbManager
import pandas as pd
import os
import logging
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np

logger = logging.getLogger(__name__)
class DataSeeder:
    def __init__(self):
        self.db_manager = DbManager()

    def seed_data(self):
        success, message = self.seed_table("sales_data.csv", Report)
        return success, message

    def process_chunk(self, chunk, copy_statement):
            """Process a single chunk of data"""
            connection = None
            cursor = None
            output = StringIO()

            try:
                connection = self.db_manager.engine.raw_connection()
                cursor = connection.cursor()
                chunk_start_time = time.time()
                logger.info(f"Processing chunk with {len(chunk)} records")

                cursor.execute("SET maintenance_work_mem = '1GB'")
                cursor.execute("SET synchronous_commit = OFF")
                cursor.execute("SET work_mem = '256MB'")

                chunk = chunk.replace({'\n': ' ', '\r': ' '})

                for column in chunk.select_dtypes(include=['float64']).columns:
                    chunk[column] = chunk[column].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else '')

                chunk.to_csv(
                    output,
                    header=False,
                    index=False,
                    sep=',',
                    lineterminator='\n',
                    quoting=1,
                    escapechar='\\',
                    na_rep=''
                )
                output.seek(0)

                cursor.copy_expert(copy_statement, output)
                connection.commit()

                chunk_time = time.time() - chunk_start_time
                logger.info(f"Chunk processed in {chunk_time:.2f} seconds")
                return len(chunk)

            except Exception as e:
                if connection:
                    connection.rollback()
                logger.error(f"Error processing chunk: {str(e)}")
                raise
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
                output.close()

    def seed_table(self, file_path, model):
        try:
            data_file = os.path.join(settings.BASE_DIR, 'core', 'data', file_path)
            db_table = model._meta.db_table

            if not os.path.exists(data_file):
                return False, f"Data file {data_file} does not exist"

            if not db_table:
                return False, f"Table name not found for model {model.__name__}"

            start_time = time.time()
            logger.info(f"Starting to seed {db_table} from {file_path}")

            df = pd.read_csv(data_file)
            logger.info(f"Loaded {len(df):,} records from CSV")


            columns = [f.name for f in model._meta.fields]

            copy_statement = f"""
                COPY {db_table} ({', '.join(columns)})
                FROM STDIN WITH (FORMAT CSV, QUOTE '"')
            """

            chunk_size = min(100000, len(df))
            cpu_count = os.cpu_count() or 1
            max_workers = min(cpu_count, 8)

            with self.db_manager.engine.connect() as conn:
                truncate_sql = text(f"TRUNCATE TABLE {db_table}")
                conn.execute(truncate_sql)
                conn.commit()


            chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(self.process_chunk, chunk, copy_statement)
                    for chunk in chunks
                ]
                results = [future.result() for future in futures]

            total_records = sum(results)
            execution_time = time.time() - start_time

            summary = (
                f"\n=== {db_table} Seeding Summary ===\n"
                f"Records: {total_records:,}\n"
                f"Time: {execution_time:.2f} seconds\n"
                f"Speed: {total_records/execution_time:,.2f} records/second"
            )
            logger.info(summary)
            return True, f"Successfully seeded {total_records:,} records in {execution_time:.2f} seconds ({total_records/execution_time:,.2f} records/second)"
        except Exception as e:
            error_msg = f"Error seeding {db_table}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg