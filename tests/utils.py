import datetime

def date_now():
    """Today's date"""
    return datetime.date.today().strftime('%Y-%m-%d')

def validate_date_now(d):
    """Test is today's date"""
    return d == datetime.date.today().strftime('%Y-%m-%d')
