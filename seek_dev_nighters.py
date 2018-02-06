import requests
from pytz import timezone
from datetime import datetime, time


API_URL = 'https://devman.org/api/challenges/solution_attempts/'


def get_number_of_pages():
    first_page = 1
    number_of_pages = requests.get(
        API_URL,
        params={'page': first_page}
    ).json()['number_of_pages']
    return number_of_pages


def load_attempts(number_of_pages):
    users_attempts = []
    for page in range(1, number_of_pages):
        users_attempts.extend(requests.get(
            API_URL,
            params={'page': page}
        ).json()['records'])
    return users_attempts


def get_local_time(tz, timestamp):
    user_timezone = timezone(tz)
    time_from_timestamp = (datetime.fromtimestamp(timestamp))
    user_local_time = user_timezone.fromutc(time_from_timestamp)
    return user_local_time


def get_midnighters(users_attempts):
    midnight = time(2, 0)
    midnighters = set()
    for record in users_attempts:
        user_local_time = get_local_time(
            record['timezone'],
            record['timestamp']
        )
        if user_local_time.time() < midnight:
            midnighters.add(record['username'])
    return midnighters


def print_midnighters(midnighters):
    if midnighters:
        for midnighter in midnighters:
            print(midnighter)
    else:
        print('No one pushed changes')


if __name__ == '__main__':
    number_of_pages = get_number_of_pages()
    users_attempts = load_attempts(number_of_pages)
    midnighters = get_midnighters(users_attempts)
    print_midnighters(midnighters)
