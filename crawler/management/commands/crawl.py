from django.core.management.base import BaseCommand
from crawler.utils import crawl

class Command(BaseCommand):
    help = 'Crawl a given URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL to crawl')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        self.stdout.write(f'Crawling {url}')
        crawl(url)
        self.stdout.write(self.style.SUCCESS('Crawling finished'))
