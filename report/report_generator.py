import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


class ReportGenerator:
    def __init__(self, title):
        self.title = title

    def generate_html(self, report_sections):
        html_content = f"<h1 style='text-align: center;'>{self.title}</h1><hr>"
        html_content += "<div style='display: flex; flex-wrap: wrap;'>"

        for subtitle, df in report_sections.items():
            html_content += "<div style='flex: 1; min-width: 300px; margin: 10px;'>"
            html_content += f"<h2 style='text-align: center;'>{subtitle}</h2>"
            html_content += df.to_html(index=False, border=0, classes='table table-striped').replace(
                '<th>', '<th style="text-align: center;">'
            )
            html_content += "</div>"

        html_content += "</div>"

        return html_content

    def generate_pdf(self, report_sections):
        try:
            pdf_stream = BytesIO()
            c = canvas.Canvas(pdf_stream, pagesize=letter)

            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(letter[0] / 2, 750, self.title)
            y_position = 720
            x_position = 50
            column_width = 250
            margin = 20

            for subtitle, df in report_sections.items():
                if x_position + column_width > letter[0] - margin:
                    x_position = 50
                    y_position -= 100

                if y_position < 100:
                    c.showPage()
                    c.setFont("Helvetica-Bold", 16)
                    c.drawCentredString(letter[0] / 2, 750, self.title)
                    y_position = 720
                    x_position = 50

                c.setFont("Helvetica-Bold", 14)
                c.drawString(x_position, y_position, subtitle)
                y_position -= 20

                c.setFont("Helvetica", 12)
                for index, row in df.iterrows():
                    if y_position < 40:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 16)
                        c.drawCentredString(letter[0] / 2, 750, self.title)
                        y_position = 720
                        x_position = 50

                    row_data = ', '.join(map(str, row))
                    c.drawString(x_position, y_position, row_data)
                    y_position -= 20

                x_position += column_width + margin

            c.save()
            pdf_stream.seek(0)
            return pdf_stream.getvalue()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None