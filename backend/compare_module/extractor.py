import re

def extract_interest(text):
    """
    Extracts the first interest rate (as a float) found in the text.
    Handles patterns like 'interest rate', 'rate of interest', 'ROI', and ranges like '6.85% to 7.05%'.
    """
    # Handle interest rate ranges like '6.85% to 7.05%'
    range_pattern = r'(\d{1,2}\.?\d{0,2})\s*%\s*(?:to|-)\s*(\d{1,2}\.?\d{0,2})\s*%'
    match = re.search(range_pattern, text, re.IGNORECASE)
    if match:
        low = float(match.group(1))
        high = float(match.group(2))
        avg = round((low + high) / 2, 2)
        return avg

    # Patterns for single interest rates
    patterns = [
        r'(?:interest rate|rate of interest|roi)[^\d]{0,20}(\d{1,2}\.?\d{0,2})\s*%',
        r'(\d{1,2}\.?\d{0,2})\s*%.*?(?:interest rate|rate of interest|roi)',
        r'(\d{1,2}\.?\d{0,2})\s*%.*?(?:p\.a\.|per annum)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    # Fallback: first percentage in text
    match = re.search(r'(\d{1,2}\.?\d{0,2})\s*%', text)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return None

def extract_lockin(text):
    """
    Extracts the lock-in period (in years, as float) from the text.
    Handles ranges like '18 to 21 months' and single values.
    """
    # Handle lock-in period ranges like '18 to 21 months'
    range_pattern = r'(?:lock[-\s]?in period|lock[-\s]?in|tenure)[^\d]{0,20}(\d{1,3})\s*(?:to|-)\s*(\d{1,3})\s*(years?|yrs?|months?|mos?)'
    match = re.search(range_pattern, text, re.IGNORECASE)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        unit = match.group(3).lower()
        avg = (low + high) / 2
        if 'month' in unit:
            return round(avg / 12, 2)
        return avg

    # Patterns for single lock-in period values
    patterns = [
        r'(?:lock[-\s]?in period|lock[-\s]?in|tenure)[^\d]{0,20}(\d{1,3})\s*(years?|yrs?|months?|mos?)',
        r'(\d{1,3})\s*(years?|yrs?|months?|mos?).{0,20}(?:lock[-\s]?in period|lock[-\s]?in|tenure)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            unit = match.group(2).lower()
            if 'month' in unit:
                return round(value / 12, 2)
            return value
    # Fallback: any 'X years' or 'X months'
    match = re.search(r'(\d{1,3})\s*(years?|yrs?|months?|mos?)', text, re.IGNORECASE)
    if match:
        value = int(match.group(1))
        unit = match.group(2).lower()
        if 'month' in unit:
            return round(value / 12, 2)
        return value
    return None
