from datetime import date

def current_date():
    return date.today().strftime("%Y-%m-%d")
