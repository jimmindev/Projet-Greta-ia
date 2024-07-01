from datetime import datetime, timedelta
import random

def generate_random_dates(number_of_dates):
    current_date = datetime.now()
    random_dates = []

    for _ in range(number_of_dates):
        random_days_ago = random.randint(1, 365)
        random_date = current_date - timedelta(days=random_days_ago)
        random_dates.append(random_date)
    return random_dates