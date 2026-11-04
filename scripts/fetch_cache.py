"""Re-download minutes PDFs/text not shipped in the package (pdf/, txt/, html/ caches were ~250MB).
Usage (from data/): python3 ../scripts/fetch_cache.py [--all]
Default: fetches every minutes_url in adcom_full_pivotal.csv into cache/pdf and cache/txt (md5(url) names, as lib.py).
Needs curl and pdftotext. Rate-limited; fda.gov and archive hosts may throttle."""
import os,sys,hashlib,pandas as pd
sys.path.insert(0,os.path.dirname(__file__)); import lib
os.makedirs('pdf',exist_ok=True); os.makedirs('txt',exist_ok=True)
U=pd.read_csv('cache/minutes_urls.csv').url.tolist()
for u in U:
    t=lib.getpdf(u); print(('ok  ' if t else 'FAIL'),u)
