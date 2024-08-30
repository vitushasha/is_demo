from django.shortcuts import render


def launch_page(request):
    return render(request, 'download_companies_in_db.html')