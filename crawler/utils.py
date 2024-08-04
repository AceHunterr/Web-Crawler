import requests
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from .models import WebPage
import json


def normaliseURL(urlString):
    parsed_url = urlparse(urlString)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    path = parsed_url.path
    trailing_string = parsed_url.query + parsed_url.fragment
    if len(trailing_string) < 2:
        path = path.rstrip('/')
    normalized_url = urlunparse((scheme, netloc, path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    print("normalized_url",normalized_url)
    return normalized_url

def fetch_page(url):
    try:
        normalized_url = normaliseURL(url)
        response = requests.get(normalized_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_page(content, base_url):
    soup = BeautifulSoup(content, 'lxml')
    title = soup.title.string if soup.title else 'No title'
    body = soup.get_text()
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    return title, body, links


def crawl(url, max_links_per_page=30, max_depth=2):
    visited = {}
    to_visit = [(url, 0)]  

    while to_visit:
        current_url, current_depth = to_visit.pop()

        if current_url not in visited:
            visited[current_url] = 0

        if visited[current_url] > 0 or current_depth > max_depth:
            visited[current_url] += 1
            continue

        visited[current_url] += 1
        content = fetch_page(current_url)
        if content:
            title, body, links = parse_page(content, current_url)

            if current_depth == 0:
                # Create or update WebPage for the initial URL
                webpage, created = WebPage.objects.get_or_create(url=current_url, defaults={'title': title, 'content': '', 'visits': 1, 'report': {}})
                if not created:
                    webpage.title = title
                    webpage.visits += 1
                    webpage.save()

            # Add a limited number of new links to the stack
            for link in links[:max_links_per_page]:
                if link.startswith('http'):
                    to_visit.append((link, current_depth + 1))

    # Save the entire report for the initial URL
    report = {url: visited_count for url, visited_count in visited.items()}
    print(json.dumps(report, indent=4))

    # Save the report in the WebPage model's `report` field for the initial URL
    initial_url = url
    try:
        webpage = WebPage.objects.get(url=initial_url)
        webpage.report = report
        webpage.save()
    except WebPage.DoesNotExist:
        # Handle the case where the initial URL WebPage instance does not exist
        print(f"Initial URL {initial_url} not found in WebPage model.")

    return report