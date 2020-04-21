import requests
import urllib


def check_url(url):
    try:
        urllib.request.urlopen(url)
    except:
        return False
    else:
        return True


def download_file(url, file_name):
    try:
        req = requests.get(url, timeout=10)
    except:
        return False
    else:
        with open(file_name, "wb") as w:
            w.write(req.content)
            w.close()
            return True
