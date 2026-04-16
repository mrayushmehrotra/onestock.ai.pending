import re
from typing import Set

# A basic list of large-cap Indian stocks for extraction baseline
COMMON_TICKERS = {
    "RELIANCE": "RELIANCE", "TCS": "TCS", "HDFC BANK": "HDFCBANK", "ICICI BANK": "ICICIBANK",
    "INFOSY": "INFY", "INFY": "INFY", "SBI": "SBIN", "BHARTI AIRTEL": "BHARTIARTL",
    "L&T": "LT", "LARSEN & TOUBRO": "LT", "ITC": "ITC", "ADANI": "ADANI",
    "TATA MOTORS": "TATAMOTORS", "TATA STEEL": "TATASTEEL", "WIPRO": "WIPRO",
    "MAHINDRA & MAHINDRA": "M&M", "M&M": "M&M", "AXIS BANK": "AXISBANK",
    "BAJAJ FINANCE": "BAJAJFINSV", "MARUTI": "MARUTI", "SUN PHARMA": "SUNPHARMA",
    "TITAN": "TITAN", "ULTRATECH": "ULTRACEMCO", "ASIAN PAINTS": "ASIANPAINT",
    "SPICEJET": "SPICEJET", "WIPRO": "WIPRO", "HYUNDAI": "HYUNDAI", "KIA": "KIA"
}

def extract_tickers(text: str) -> Set[str]:
    found = set()
    text_upper = text.upper()
    for name, ticker in COMMON_TICKERS.items():
        if name in text_upper:
            found.add(ticker)
    
    # Also look for patterns like (NSE: ...) or (BSE: ...)
    patterns = [r'NSE:\s*([A-Z]+)', r'BSE:\s*([0-9A-Z]+)']
    for pattern in patterns:
        matches = re.findall(pattern, text_upper)
        for match in matches:
            found.add(match)
            
    return found

if __name__ == "__main__":
    sample = "SpiceJet hits upper circuit again; Wipro and HDFC Bank stocks are in focus ahead of Q4 results."
    print(f"Extracted: {extract_tickers(sample)}")
