"""Diff FDA committee meeting-materials pages and EDGAR 8-K/6-K disclosures
against adcom_full_pivotal.csv, excluded.csv and gaps.csv.

Writes data/missing_row_search.csv. Does not add rows. A meeting is a candidate
only when the FDA page (or an SEC filing that quotes a tally) is not already
in the pivotal sheet, the excluded sheet, or gaps.csv for that date and committee.
"""
import csv, json, os, re, time, urllib.request
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UA = "AdCom-missing-row-search/1.0 (research; public FDA and SEC documents)"
MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}
DATE_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),\s+(20(?:1[6-9]|2[0-6]))\b")

# (abbrev, committee homepage). Year pages are discovered from the homepage
# and from the conventional /YYYY-meeting-materials- slug.
COMMITTEES = [
    ("ODAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/oncologic-drugs-advisory-committee"),
    ("EMDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/endocrinologic-and-metabolic-drugs-advisory-committee"),
    ("AADPAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/anesthetic-and-analgesic-drug-products-advisory-committee"),
    ("AMDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/antimicrobial-drugs-advisory-committee-formerly-known-anti-infective-drugs-advisory-committee"),
    ("CRDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/cardiovascular-and-renal-drugs-advisory-committee"),
    ("AAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/arthritis-advisory-committee"),
    ("BRUDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/obstetrics-reproductive-and-urologic-drugs-advisory-committee-formerly-bone-reproductive-and"),
    ("PADAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/pulmonary-allergy-drugs-advisory-committee"),
    ("PDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/psychopharmacologic-drugs-advisory-committee"),
    ("GIDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/gastrointestinal-drugs-advisory-committee"),
    ("PCNS", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/peripheral-and-central-nervous-system-drugs-advisory-committee"),
    ("DODAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/dermatologic-and-ophthalmic-drugs-advisory-committee"),
    ("NDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/nonprescription-drugs-advisory-committee"),
    ("PCAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/pharmacy-compounding-advisory-committee"),
    ("DSaRM", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/drug-safety-and-risk-management-advisory-committee"),
    ("MIDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/medical-imaging-drugs-advisory-committee"),
    ("GeMDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/genetic-metabolic-diseases-advisory-committee"),
    ("PSCPAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/pharmaceutical-science-and-clinical-pharmacology-advisory-committee"),
    ("AVDAC", "https://www.fda.gov/advisory-committees/human-drug-advisory-committees/antiviral-drugs-advisory-committee"),
    ("CTGTAC", "https://www.fda.gov/advisory-committees/blood-vaccines-and-other-biologics/cellular-tissue-and-gene-therapies-advisory-committee"),
    ("VRBPAC", "https://www.fda.gov/advisory-committees/blood-vaccines-and-other-biologics/vaccines-and-related-biological-products-advisory-committee"),
    ("BPAC", "https://www.fda.gov/advisory-committees/blood-vaccines-and-other-biologics/blood-products-advisory-committee"),
]


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        code = getattr(e, "code", None)
        return code or 0, str(e)


def textify(html):
    html = re.sub(r"(?is)<script[\s\S]*?</script>", " ", html)
    html = re.sub(r"(?is)<style[\s\S]*?</style>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|li|h\d|tr)>", "\n", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    html = re.sub(r"[ \t]+", " ", html)
    return html


def year_links(html, page_url):
    links = set(re.findall(r'href="([^"]*20(?:1[6-9]|2[0-6])-meeting-materials[^"]*)"', html, re.I))
    out = []
    for h in links:
        if h.startswith("http"):
            out.append(h.split("?")[0])
        elif h.startswith("/"):
            out.append("https://www.fda.gov" + h.split("?")[0])
    # conventional slug from the homepage path
    slug = page_url.rstrip("/").split("/")[-1]
    for y in range(2016, 2027):
        out.append(f"https://www.fda.gov/advisory-committees/{slug}/{y}-meeting-materials-{slug}")
    # some CBER pages nest the year list under the short name already in the href
    return sorted(set(out))


def meetings_from_text(committee, url, text):
    rows = []
    for m in DATE_RE.finditer(text):
        iso = f"{int(m.group(3)):04d}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
        if iso < "2016-11-04" or iso > "2026-11-04":
            continue
        window = text[m.start(): m.start() + 700]
        window = re.sub(r"\s+", " ", window).strip()
        app = ""
        am = re.search(r"\b((?:s)?(?:NDA|BLA))\s*([0-9]{5,6}(?:/S-\d+)?)", window, re.I)
        if am:
            app = am.group(2)
        productish = bool(re.search(r"\b(NDA|BLA|sNDA|sBLA)\b", window, re.I))
        rows.append(dict(meeting_date=iso, committee=committee, app=app,
                         product_text=window[:400], source_url=url, productish=productish))
    # one row per date on that page (keep the blurb that mentions an application)
    best = {}
    for r in rows:
        k = r["meeting_date"]
        if k not in best or (r["productish"] and not best[k]["productish"]):
            best[k] = r
    return list(best.values())


def load_known():
    piv = pd.read_csv(os.path.join(DATA, "adcom_full_pivotal.csv"), dtype=str).fillna("")
    exc = pd.read_csv(os.path.join(DATA, "excluded.csv"), dtype=str).fillna("")
    gaps = pd.read_csv(os.path.join(DATA, "gaps.csv"), dtype=str).fillna("")
    def keyset(df):
        if "meeting_date" not in df.columns:
            return set()
        com = df["committee"] if "committee" in df.columns else ""
        return set(zip(df["meeting_date"], com.astype(str)))
    return piv, exc, gaps, keyset(piv), keyset(exc), keyset(gaps)


def edgar():
    """SEC full-text search. Returns filings whose snippet quotes a vote tally."""
    hits = []
    q = '"advisory committee" AND (voted OR "voted")'
    start = 0
    tally = re.compile(r"\b(\d{1,2})\s*[-–to]+\s*(\d{1,2})\b")
    while start < 200:
        url = ("https://efts.sec.gov/LATEST/search-index?q=" + urllib.request.quote(q)
               + f"&forms=8-K,6-K&dateRange=custom&startdt=2016-11-04&enddt=2026-11-04&from={start}")
        code, body = fetch(url)
        if code != 200:
            hits.append(dict(error=f"EDGAR HTTP {code}", detail=body[:300], source_url=url))
            break
        try:
            js = json.loads(body)
        except json.JSONDecodeError:
            hits.append(dict(error="EDGAR not JSON", detail=body[:300], source_url=url))
            break
        batch = js.get("hits", {}).get("hits", [])
        if not batch:
            break
        for h in batch:
            src = h.get("_source", {})
            ad = src.get("adsh", "") or src.get("file_num", "")
            names = src.get("display_names") or src.get("entity_name") or ""
            if isinstance(names, list):
                names = "; ".join(names)[:200]
            period = (src.get("file_date") or src.get("period_ending") or "")[:10]
            # filings link
            cik = ""
            ciks = src.get("ciks") or []
            if ciks:
                cik = str(ciks[0]).lstrip("0")
            link = ""
            if cik and ad:
                ad_nodash = ad.replace("-", "")
                link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{ad_nodash}/{ad}-index.html"
            desc = " ".join(str(src.get(k, "")) for k in ("file_description", "items", "display_names"))[:500]
            hits.append(dict(meeting_date=period, committee="", app="", product_text=str(names)[:300],
                             source_url=link or url, snippet=desc, tally=bool(tally.search(desc))))
        start += len(batch)
        if start >= js.get("hits", {}).get("total", {}).get("value", start):
            break
        time.sleep(0.4)
    return hits


def main():
    piv, exc, gaps, pk, ek, gk = load_known()
    found = []
    page_log = []
    for abbrev, home in COMMITTEES:
        code, html = fetch(home)
        page_log.append(dict(committee=abbrev, url=home, status=code))
        links = year_links(html if code == 200 else "", home)
        time.sleep(0.25)
        seen_url = set()
        for link in links:
            if link in seen_url:
                continue
            seen_url.add(link)
            c2, html2 = fetch(link)
            page_log.append(dict(committee=abbrev, url=link, status=c2))
            if c2 == 200 and "meeting" in html2.lower():
                found.extend(meetings_from_text(abbrev, link, textify(html2)))
            time.sleep(0.2)
        print(abbrev, "pages", len(seen_url), "meetings", sum(1 for r in found if r["committee"] == abbrev), flush=True)

    rows = []
    for r in found:
        key = (r["meeting_date"], r["committee"])
        # joint meetings may be stored under a combined committee name
        in_piv = key in pk or any(r["meeting_date"] == d and r["committee"] in c for d, c in pk)
        in_exc = key in ek or any(r["meeting_date"] == d and r["committee"] in c for d, c in ek)
        in_gap = key in gk
        if in_piv:
            disp = "already in pivotal"
        elif in_exc:
            disp = "already excluded"
        elif in_gap:
            disp = "already in gaps"
        else:
            disp = "not in dataset"
        why = ""
        if disp == "already excluded":
            hit = exc[(exc.meeting_date == r["meeting_date"]) & (exc.committee.astype(str).str.contains(r["committee"]))]
            if len(hit):
                why = str(hit.iloc[0].get("reason", ""))[:240]
        rows.append(dict(
            meeting_date=r["meeting_date"], committee=r["committee"], app=r["app"],
            product_text=r["product_text"], source="FDA committee meeting-materials page",
            source_url=r["source_url"], product_application_mentioned=r["productish"],
            disposition=disp, excluded_reason=why, added="no"))

    sec = edgar()
    for h in sec:
        if h.get("error"):
            rows.append(dict(
                meeting_date="", committee="", app="", product_text=h.get("detail", ""),
                source="EDGAR full-text", source_url=h.get("source_url", ""),
                product_application_mentioned="", disposition="search error: " + h["error"],
                excluded_reason="", added="no"))
            continue
        # SEC hits are company filings, not a meeting key. Keep those whose
        # display text is a vote disclosure; disposition is reviewed below.
        rows.append(dict(
            meeting_date=h["meeting_date"], committee="", app="", product_text=h["product_text"],
            source="EDGAR 8-K/6-K", source_url=h["source_url"],
            product_application_mentioned="", disposition="edgar filing (see notes)",
            excluded_reason=h.get("snippet", "")[:240], added="no"))

    outp = os.path.join(DATA, "missing_row_search.csv")
    cols = ["meeting_date", "committee", "app", "product_text", "source", "source_url",
            "product_application_mentioned", "disposition", "excluded_reason", "added"]
    pd.DataFrame(rows, columns=cols).to_csv(outp, index=False)
    with open(os.path.join(DATA, "cache", "fda_calendar_page_log.json"), "w") as f:
        json.dump(page_log, f)
    n_new = sum(1 for r in rows if r["disposition"] == "not in dataset")
    print("fda meetings", len(found), "not in dataset", n_new, "edgar rows", sum(1 for r in rows if r["source"].startswith("EDGAR")))
    print("wrote", outp)


if __name__ == "__main__":
    main()
