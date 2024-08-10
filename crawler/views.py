import json
from django.shortcuts import render
from django.http import JsonResponse
from .utils import crawl


from django.views.decorators.csrf import csrf_exempt
from .models import WebPage
from .utils import crawl


def start_crawl(request, url_name):
    initial_url = f"https://{url_name}"
    report = crawl(initial_url)
    return JsonResponse(report)

def index(request):
    return render(request, 'index.html')

def search_page(request):
    return render(request, 'search.html')

@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        keyword = data.get('keyword')
        url = data.get('url')

        # Assuming the crawl has already happened before this
        webpages = WebPage.objects.filter(content__icontains=keyword)
        results = [webpage.url for webpage in webpages]

        return JsonResponse({'results': results})

    return JsonResponse({'results': []})