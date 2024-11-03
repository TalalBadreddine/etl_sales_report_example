from sqlalchemy import create_engine


from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

class DbManager:
    def __init__(self):
        load_dotenv()
        DATABASE_URL = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

        print("DB URL: ", DATABASE_URL)

        self.engine = create_engine(
            DATABASE_URL,
            pool_size=15,
            max_overflow=30
        )

    def get_engine(self):
        return self.engine