from django.http import HttpResponse
from django.shortcuts import render
from sales_etl.decorators.description import document_url
from core.data_seeder import DataSeeder

def handler404(request, exception=None):
    url_patterns = {
        '': 'Home page that also seeds the database with sample data',
        'reports/': 'Generates the main report',
        'admin': 'Django admin interface',
    }

    current_path = request.path.lstrip('/')

    context = {
        'current_path': current_path,
        'available_paths': [
            {
                'url': path,
                'full_url': request.build_absolute_uri('/' + path),
                'description': desc
            }
            for path, desc in url_patterns.items()
        ]
    }

    return render(request, '404.html', context, status=404)

@document_url("Fills the database with sample data")
def fillDb(request):
    data_seeder = DataSeeder()
    success, message =  data_seeder.seed_data()
    print(success, message)
    if not success:
        return HttpResponse(message, status=500)

    return HttpResponse(message)
