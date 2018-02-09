import requests
from pytz import timezone
from datetime import datetime


def load_attempts():
    page = 1
    while True:
        users_attempts = requests.get(
            'https://devman.org/api/challenges/solution_attempts/',
            params={'page': page}
        )

        for attempt in users_attempts.json()['records']:
            yield attempt

        if page >= users_attempts.json()['number_of_pages']:
            break
        else:
            page += 1


def is_midnighter(attempt):
    midnight = 2
    user_local_time = datetime.fromtimestamp(
        attempt['timestamp'],
        timezone(attempt['timezone'])
    )
    return user_local_time.hour < midnight


def print_midnighters(midnighters):
    if midnighters:
        print('Midnigters are:')
        for midnighter in midnighters:
            print(midnighter)
    else:
        print('No one pushed changes')


if __name__ == '__main__':
    midnighters = set()
    for attempt in load_attempts():
        if is_midnighter(attempt):
            midnighters.add(attempt['username'])
    print_midnighters(midnighters)
