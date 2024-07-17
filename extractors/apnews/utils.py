import os
import re
import shutil
import uuid
from datetime import datetime, date, timedelta

import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta

from extractors import AMOUNT_REGEX
from logging_config import logger


def get_till_date(number_of_months: int) -> date:
    """
    Get the date for a given number of months ago from the current date.
    Defaults to one month ago if number_of_months is 0.

    Args:
    - number_of_months (int): The number of months to go back.

    Returns:
    - date: The calculated past date.
    """
    if number_of_months == 0:
        number_of_months = 1
    return (datetime.now() - relativedelta(months=number_of_months)).date()


def contains_amount(title: str, description: str) -> bool:
    """
    Check if the given title or description contains any monetary amount.

    Args:
    - title (str): The title of the news item.
    - description (str): The description of the news item.

    Returns:
    - bool: True if any monetary amount is found, False otherwise.
    """
    return bool(re.findall(AMOUNT_REGEX, f"{title} {description}", re.IGNORECASE))


def count_search_phrase(title: str, description: str, phrase: str) -> int:
    """
    Count the occurrences of a search phrase in the title and description.

    Args:
    - title (str): The title of the news item.
    - description (str): The description of the news item.
    - phrase (str): The search phrase to count.

    Returns:
    - int: The count of search phrase occurrences.
    """
    return len(re.findall(re.escape(phrase), f"{title} {description}", re.IGNORECASE))


def parse_date(date_str: str) -> str | None:
    """
    Parse a date string into an ISO format date string.
    Handles relative dates like "5 mins ago" and "Yesterday".

    Args:
    - date_str (str): The date string to parse.

    Returns:
    - str | None: The parsed ISO format date string, or None if parsing fails.
    """

    if 'min' in date_str:
        minutes = int(date_str.split(' ')[0])
        return (datetime.now() - timedelta(minutes=minutes)).date().isoformat()

    if 'hour' in date_str:
        hours = int(date_str.split(' ')[0])
        return (datetime.now() - timedelta(hours=hours)).date().isoformat()

    if date_str.lower() == 'yesterday':
        return (datetime.now() - timedelta(days=1)).date().isoformat()

    try:
        return parser.parse(date_str).date().isoformat()
    except (ValueError, OverflowError):
        return None


def reached_date_limit(till_date: date, last_item_date: str | None) -> bool:
    """
    Check if the last item date is beyond the specified till date.

    Args:
    - till_date (date): The date limit.
    - last_item_date (str | None): The date of the last item.

    Returns:
    - bool: True if the last item date is beyond the till date, False otherwise.
    """
    if last_item_date:
        last_item_date = datetime.strptime(last_item_date, '%Y-%m-%d').date()
        return till_date > last_item_date
    return False


def make_archive(source: str, destination: str, remove_source=True) -> None:
    """
    Create a zip archive of the specified source directory and save it to the destination.
    Optionally remove the source directory after archiving.

    Args:
    - source (str): The source directory to archive.
    - destination (str): The destination path for the archive.
    - remove_source (bool): Whether to remove the source directory after archiving.
    """
    shutil.make_archive(source, 'zip', destination)
    if remove_source:
        try:
            shutil.rmtree(source)
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to remove directory='{source}' image. Error: {e}")


def generate_filename() -> str:
    """
    Generate a random filename with a .png extension.

    Returns:
    - str: The generated filename.
    """
    return f"{uuid.uuid4().hex}.png"


def download_by_image_url(output_dir: str, url: str) -> str | None:
    """
    Download an image from a given URL and save it to the specified output directory.

    Args:
    - output_dir (str): The directory to save the downloaded image.
    - url (str): The URL of the image to download.

    Returns:
    - str | None: The filename of the downloaded image, or None if download fails.
    """
    if not url:
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join(output_dir, generate_filename())
            with open(file_name, "wb") as file:
                file.write(response.content)
            return file_name
    except Exception as e:
        logger.error(f"Failed to download image. Error: {e}")
    return None
