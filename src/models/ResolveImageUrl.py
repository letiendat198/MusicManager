import urllib3

def get_data_from_url(url, progress_callback=None):
    http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=2.0, read=2.0))
    resp = http.request("GET", url)
    return resp.data