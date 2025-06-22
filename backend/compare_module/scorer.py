def score(data, user_prefs, product_type="loan"):
    """
    Scores a product (loan or FD) based on extracted fields and user preferences.
    - For loans: lower interest and lower lock-in are better.
    - For FDs: higher interest is better, lower lock-in is better (unless user prefers otherwise).
    Returns a score between 0 and 10.
    """
    score = 0
    # Interest scoring
    if data['interest'] is not None:
        if product_type == "loan":
            # Lower is better
            max_interest = user_prefs.get('max_interest', 100)
            min_interest = user_prefs.get('min_interest', 0)
            if data['interest'] <= min_interest:
                interest_score = 1.0
            elif data['interest'] >= max_interest:
                interest_score = 0.0
            else:
                interest_score = (max_interest - data['interest']) / (max_interest - min_interest)
            score += interest_score * 6  # Weight: 6/10
        elif product_type == "fd":
            # Higher is better
            max_interest = user_prefs.get('max_interest', 20)  # 20% is a safe upper bound for FDs
            min_interest = user_prefs.get('min_interest', 0)
            if data['interest'] >= max_interest:
                interest_score = 1.0
            elif data['interest'] <= min_interest:
                interest_score = 0.0
            else:
                interest_score = (data['interest'] - min_interest) / (max_interest - min_interest)
            score += interest_score * 6  # Weight: 6/10

    # Lock-in scoring (lower is better)
    if data['lockin'] is not None:
        max_lockin = user_prefs.get('max_lockin', 100)
        min_lockin = user_prefs.get('min_lockin', 0)
        if data['lockin'] <= min_lockin:
            lockin_score = 1.0
        elif data['lockin'] >= max_lockin:
            lockin_score = 0.0
        else:
            lockin_score = (max_lockin - data['lockin']) / (max_lockin - min_lockin)
        score += lockin_score * 4  # Weight: 4/10

    return round(score, 2)
