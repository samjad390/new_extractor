from typing import Optional

from pydantic import BaseModel, computed_field

from extractors.apnews.utils import contains_amount, count_search_phrase


class APNewsItem(BaseModel):
    """
    APNewsItem represents a news item from the AP News site.

    Attributes:
        id (int): Unique identifier for the news item.
        title (str): Title of the news item.
        description (str): Description of the news item.
        date (Optional[str]): Publication date of the news item.
        image (Optional[str]): URL of the news item's image.
        search_phrase (str): Search phrase used to find the news item.
        image_name (str | None): image name of the news item.
    """

    id: int
    title: Optional[str]
    description: Optional[str]
    date: Optional[str]
    image: Optional[str]
    search_phrase: str
    image_name: Optional[str]

    @computed_field
    def containing_amount(self) -> bool:
        """
        Check if the title or description contains an amount.

        Returns:
            bool: True if an amount is found, False otherwise.
        """
        return contains_amount(self.title, self.description)

    @computed_field
    def count_of_search_phrase(self) -> int:
        """
        Count the occurrences of the search phrase in the title and description.

        Returns:
            int: The number of times the search phrase appears.
        """
        return count_search_phrase(self.title, self.description, self.search_phrase)
