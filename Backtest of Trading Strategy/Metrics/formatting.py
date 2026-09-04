#Formatting, make the number and def readable in the dashboard

def format_pct(value):
    """Changing number in to %"""
    value = f"{value * 100:.2f}%"
    return value

def format_points(value):
    """Changing number in to pts"""
    value = f"{value:.2f} pts"
    return value

def format_min(value):
    """Format TimeDelta in min """
    value = f'{value.total_seconds() / 60:.2f} min'
    return value
