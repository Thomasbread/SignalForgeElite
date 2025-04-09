def format_price(price, pair=""):
    """
    Format price according to currency pair
    
    Parameters:
    price (float): The price to format
    pair (str): The currency pair (optional)
    
    Returns:
    str: Formatted price
    """
    if 'JPY' in pair:
        # JPY pairs typically have 2 decimal places
        return f"{price:.2f}"
    else:
        # Most forex pairs have 4 or 5 decimal places
        return f"{price:.5f}"
