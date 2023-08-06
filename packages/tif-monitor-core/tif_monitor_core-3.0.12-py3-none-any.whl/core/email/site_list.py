from datetime import datetime

sites = {}


def send_for_brand( brand, suppression_time):
    current_time = datetime.today()
    if brand in sites:
        time_diff = current_time - sites[brand]
        send_email = time_diff.total_seconds() > suppression_time
        return send_email
    else:
        return True


def update_last_email_time(brand):
    sites[brand] = datetime.today()
