import sys
import logging

from lib import spreadsheet_storage


def fetch_champions():
    """
    The function fetches the list of champions from the storage.
    The "champions" is a name of sheet in "twizy" Google Sheets document.
    """
    champions = [
        (name, int(score), int(time)) for name, score,
        time in spreadsheet_storage.get_table("champions")[1:]
    ]
    logging.info(f"Champions: {champions}")

    return champions


def update_champions(new_champions):
    """
    Updates the champions list in the storage.
    The "champions" is a name of sheet in "twizy" Google Sheets document.
    """
    spreadsheet_storage.set_table("champions", new_champions)


def turn_index_into_place(index):
    """
    Converts a zero-based index into a one-based place ranking.
    """
    if index == -1:
        return -1

    return index + 1


def record_user_score(username, score, timestamp):
    """
    Records a user's score in the champions list, updating it as necessary.
    """
    champions = fetch_champions()
    max_champions = len(champions)
    applicant = (username, score, timestamp)

    exist_index = next((i for i, c in enumerate(champions)
                       if c == applicant), -1)
    if exist_index != -1:
        return turn_index_into_place(exist_index)

    # Add the new score and sort the list by score in descending order
    champions.append(applicant)
    champions.sort(key=lambda c: c[1], reverse=True)

    new_champions = champions[:max_champions]
    update_champions(new_champions)

    # Find the new index of the applicant in the updated list
    i = next((i for i, c in enumerate(new_champions) if c == applicant), -1)

    return turn_index_into_place(i)
