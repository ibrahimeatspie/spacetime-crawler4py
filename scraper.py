import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if resp.status!=200:
        return list()
    html = resp.raw_response.content
    # html_bytes = html.encode('utf-8')
    res = []

    soup = BeautifulSoup(html, 'html.parser')
    urls = [link.get('href') for link in soup.find_all('a') if link.get('href')]
    link_urls = [link.get('href') for link in soup.find_all('link') if link.get('href')]
    allURLS = urls+link_urls
    for url in allURLS:
        if is_valid(url):
            res.append(url)

    return res    


    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return list()

def is_valid(url):
    validUrls = set([".cs.uci.edu/",
        ".ics.uci.edu/",
        ".informatics.uci.edu/",
        ".stat.uci.edu/",
        "today.uci.edu/department/information_computer_sciences/"
     ])

    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        stringUrl = parsed.netloc+parsed.path
        for validUrl in validUrls:
            if validUrl in stringUrl:
                return True  
                
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
