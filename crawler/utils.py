from urllib.parse import urlparse,urlunparse



def normaliseURL(urlString):
    parsed_url = urlparse(urlString)
    print("parsed_url: ", parsed_url)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    path = parsed_url.path
    trailing_string = parsed_url.query + parsed_url.fragment
    if(len(trailing_string) < 2):
        path = path.rstrip('/')
    
    normalized_url = urlunparse((scheme, netloc, path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    stripped_url = normalized_url.replace(f"{scheme}://", "", 1)
    print("unparsed_url: ", stripped_url)
    return stripped_url
