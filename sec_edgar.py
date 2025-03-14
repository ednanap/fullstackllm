import requests

class SecEdgar:
    BASE_URL = "https://data.sec.gov/submissions/CIK{}.json"
    def __init__(self, fileUrl, user_agent="Swarthmore enapoli1@swarthmore.edu"):
        self.fileUrl = fileUrl
        self.headers = {"User-Agent": user_agent}
        self.nameDict = {}
        self.tickerDict = {}
        
        try:
            self.p = requests.get(self.fileUrl, headers=self.headers)
            self.filejson = self.p.json()
            self._load_data()
        except Exception as e:
            raise Exception(f"Failed to fetch SEC data: {e}")
    
    def _load_data(self):
        """Loads company data from the provided file URL."""
        for entry in self.filejson.values():
            company_name = entry['title'].strip()
            ticker = entry.get('ticker', '').strip()
            cik = str(entry['cik_str']).zfill(10)  # Ensure CIK is 10 digits
            
            self.nameDict[company_name.lower()] = (ticker, cik)
            if ticker:
                self.tickerDict[ticker.upper()] = (company_name, cik)
    
    def _fetch_filings(self, cik):
        """Fetches company filings from SEC."""
        cik = str(cik).zfill(10)  # Ensure CIK is 10 digits
        url = self.BASE_URL.format(cik)

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch SEC filings for CIK {cik}")

    def _find_filing(self, cik, year, form_type, quarter=None):
        """Finds the latest filing (10-K or 10-Q) for a given year."""
        data = self._fetch_filings(cik)
        filings = data.get("filings", {}).get("recent", {})

        for i in range(len(filings["form"])):
            if filings["form"][i] == form_type:
                filing_date = filings["filingDate"][i]
                filing_year = int(filing_date[:4])

                if filing_year == year:
                    if form_type == "10-Q" and quarter is not None:
                        filing_quarter = (int(filing_date[5:7]) - 1) // 3 + 1
                        if filing_quarter != quarter:
                            continue  # Skip if not the correct quarter

                    accession = filings["accessionNumber"][i].replace("-", "")
                    primary_doc = filings["primaryDocument"][i]  # Extract actual filing document
                    filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primary_doc}"

                    return filing_url

        return "No filing found for the given year (and quarter, if applicable)."

    def name_to_cik(self, name):
        """Returns CIK for a given company name."""
        return self.nameDict.get(name.lower(), "Entry not found")

    def ticker_to_cik(self, ticker):
        """Returns CIK for a given stock ticker."""
        return self.tickerDict.get(ticker.upper(), "Entry not found")

    def annual_filing(self, cik, year):
        """Returns the URL for the 10-K annual filing for a given CIK and year."""
        return self._find_filing(cik, year, "10-K")

    def quarterly_filing(self, cik, year, quarter):
        """Returns the URL for the 10-Q quarterly filing for a given CIK, year, and quarter (1-4)."""
        if quarter not in [1, 2, 3, 4]:
            return "Invalid quarter. Must be 1, 2, 3, or 4."
        return self._find_filing(cik, year, "10-Q", quarter)
        
        # print(self.p.text)
if __name__ == "__main__":
    sec_url = "https://www.sec.gov/files/company_tickers.json"

    # Create an instance of SecEdgar
    sec_lookup = SecEdgar(sec_url)

    # Test name_to_cik() - Example with Apple Inc.
    company_name = "Apple Inc."
    cik_info = sec_lookup.name_to_cik(company_name)
    print(f"CIK Lookup for {company_name}: {cik_info}")

    # Test ticker_to_cik() - Example with AAPL (Apple Inc. ticker)
    ticker = "AAPL"
    cik_info = sec_lookup.ticker_to_cik(ticker)
    print(f"CIK Lookup for ticker {ticker}: {cik_info}")

    # Test annual_filing() - Fetch Apple's 10-K for 2023
    cik = "0000320193"  # Apple's CIK (Zero-padded to 10 digits)
    year = 2023
    annual_filing_url = sec_lookup.annual_filing(cik, year)
    print(f"Annual 10-K Filing for {company_name} ({year}): {annual_filing_url}")

    # Test quarterly_filing() - Fetch Apple's Q2 10-Q for 2023
    quarter = 2  # Choose quarter 1-4
    quarterly_filing_url = sec_lookup.quarterly_filing(cik, year, quarter)
    print(f"Quarterly 10-Q Filing for {company_name}, Q{quarter} {year}: {quarterly_filing_url}")
