import sys
import logging
from lib import spreadsheet_storage


def fetch_champions():
    champions = [
        (name, int(score), int(time)) for name, score,
        time in spreadsheet_storage.get_table("champions")[1:]
    ]
    logging.info(f"CHAMPIONS: {champions}")

    return champions


def update_champions(new_champions):
    spreadsheet_storage.set_table("champions", new_champions)


def turn_index_into_place(index):
    if index == -1:
        return -1

    return index + 1


def record_user_score(username, score, timestamp):
    champions = fetch_champions()
    max_champions = len(champions)
    applicant = (username, score, timestamp)

    exist_index = next((i for i, c in enumerate(champions)
                       if c == applicant), -1)
    if exist_index != -1:
        return turn_index_into_place(exist_index)

    champions.append(applicant)
    champions.sort(key=lambda c: c[1], reverse=True)

    new_champions = champions[:max_champions]
    update_champions(new_champions)

    i = next((i for i, c in enumerate(new_champions) if c == applicant), -1)

    return turn_index_into_place(i)
