from django.db import models

class Report(models.Model):
    transaction_id = models.IntegerField(unique=True, primary_key=True)
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity_sold = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    date_sold = models.DateField()
    customer_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Report {self.transaction_id}"

    class Meta:
        db_table = 'report'
