from django.db import connection
import pandas as pd

class ReportService:
    def __init__(self):
        pass

    def generate_report(self, start_date=None, end_date=None, n=5):
        try:
            top_products = self.get_top_products_sold(n=n, start_date=start_date, end_date=end_date)
            profit_leaders = self.get_top_products_by_profit(n=n, start_date=start_date, end_date=end_date)
            price_data = self.get_top_products_by_unit_price(n=n)
            product_counts = self.get_product_counts(n=n)
            quartile_by_price = self.get_products_in_quartile_by_price(quartile=4, n=n, start_date=start_date, end_date=end_date)
            quartile_by_quantity = self.get_products_in_quartile_by_quantity(quartile=4, n=n, start_date=start_date, end_date=end_date)

            report_sections = {
                'Top Products by Sales Volume': pd.DataFrame(
                    top_products, columns=['Product', 'Quantity Sold']
                ),
                'Top Products by Profit': pd.DataFrame(
                    profit_leaders, columns=['Product', 'Profit in $']
                ),
                'Top Products by Unit Price': pd.DataFrame(
                    price_data, columns=['Product', 'Unit Price in $']
                ),
                'Product Inventory Counts': pd.DataFrame(
                    product_counts, columns=['Product', 'Product Count']
                ),
                'Products in Fourth Quartile by Price': pd.DataFrame(
                    quartile_by_price, columns=['Product', 'Total Price']
                ),
                'Products in Fourth Quartile by Quantity': pd.DataFrame(
                    quartile_by_quantity, columns=['Product', 'Quantity Sold']
                )
            }

            return report_sections
        except Exception as e:
            print("ERROR: ", e)
            raise e
    def get_top_products_sold(self, n=5, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM get_top_n_products_sold(%s, %s, %s)",
                [n, start_date, end_date]
            )
            return cursor.fetchall()

    def get_top_products_by_profit(self, n=5, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM get_top_n_products_by_profit(%s, %s, %s)",
                [n, start_date, end_date]
            )
            results = cursor.fetchall()
            formatted_results = [(product, f"${profit}") for product, profit in results]
            return formatted_results

    def get_top_products_by_unit_price(self, n=5):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM get_top_n_products_by_unit_price(%s)",
                [n]
            )
            results = cursor.fetchall()
            formatted_results = [(product, f"${unit_price}") for product, unit_price in results]
            return formatted_results

    def get_product_counts(self, n=5):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM get_count_of_products_by_name(%s)",
                [n]
            )
            return cursor.fetchall()

    def get_products_in_quartile_by_price(self, quartile=4, n=5, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM get_products_in_n_quartile_by_total_price(
                    %s, %s, %s::DATE, %s::DATE
                )
                """,
                [quartile, n, start_date, end_date]
            )
            return cursor.fetchall()

    def get_products_in_quartile_by_quantity(self, quartile=4, n=5, start_date=None, end_date=None):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM get_nth_quartile_by_quantity_sold(
                    %s, %s, %s::DATE, %s::DATE
                )
                """,
                [quartile, n, start_date, end_date]
            )
            return cursor.fetchall()