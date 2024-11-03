from sre_constants import SUCCESS
from django.http  import HttpResponse
from core.data_seeder import DataSeeder
from .s3_manager import S3Manager
from .report_generator import ReportGenerator
from sales_etl.decorators.description import document_url
from .report_service import ReportService
from datetime import datetime, timedelta

@document_url("Generates the main report")
def generate_main_report(request):
    try:
        report_service = ReportService()
        dfs_dict = report_service.generate_report()
        report_generator = ReportGenerator("Main Report")
        htmlPage = report_generator.generate_html(dfs_dict)
        pdfPage = report_generator.generate_pdf(dfs_dict)

        current_datetime = datetime.today().strftime('%Y-%m-%d_%H-%M')
        filename = f"main_report_{current_datetime}.pdf"

        s3_manager = S3Manager()
        s3_manager.upload_file(pdfPage, filename)
        return HttpResponse(htmlPage)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def generate_last_month_report(request):
    try:
        today = datetime.today()
        first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = first_day_of_current_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        last_month_start_date = last_month_start.date()
        last_month_end_date = last_month_end.date()

        report_service = ReportService()
        dfs_dict = report_service.generate_report(start_date=last_month_start_date, end_date=last_month_end_date)
        report_generator = ReportGenerator("Last Month Report")
        htmlPage = report_generator.generate_html(dfs_dict)
        return HttpResponse(htmlPage)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)