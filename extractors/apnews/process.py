import os.path

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from extractors.apnews import ApNewsLocators, APNewsItem, parse_date, reached_date_limit, get_till_date, download_by_image_url, make_archive
from extractors import BrowserWrapper, retry


from logging_config import logger


class ApNews(BrowserWrapper, ApNewsLocators):
    """
    Class to extract news articles from AP News website.

    Attributes:
    - base_url (str): The base URL of the AP News website.
    - search_phrase (str): The phrase to search for in the news articles.
    - category (str): The category of news articles to filter by.
    - news_count (int): Counter for the number of news articles extracted.
    - output_dir (str): Directory to save the extracted data.
    - results (list): List to store the extracted news items.
    - till_date (datetime): Date limit for extracting news articles.
    """

    def __init__(self, search_phrase: str, no_of_months: int, category: str) -> None:
        """
        Initialize the ApNews object with search phrase, number of months, and category.

        Args:
        - search_phrase (str): The phrase to search for in the news articles.
        - no_of_months (int): The number of months to go back from the current date.
        - category (str): The category of news articles to filter by.
        """
        self.base_url = "https://apnews.com/"
        self.search_phrase = search_phrase
        self.category = category
        self.news_count = 0
        self.output_dir = 'output'
        self.results = []
        self.till_date = get_till_date(no_of_months)

        # Creating directory structure
        self.create_directory_structure()

        super().__init__()

    def create_directory_structure(self) -> None:
        """
        Create the directory structure for saving the output data.
        """
        os.makedirs(self.output_dir, exist_ok=True)

    @retry(retries=3, delay=2)
    def close_donation_popup_by_cross(self) -> None:
        """
        Close the donation popup if it appears on the page.
        """
        self.click_element_when_visible(self.DONATION_POP_CROSS_LOCATOR, timeout=30)
        logger.info('Closed Donation Popup')

    def accept_cookies(self) -> None:
        """
        Accepting Cookies if it appears on the page.
        """
        try:
            self.click_element_when_visible(self.COOKIES_LOCATOR, timeout=30)
            logger.info('Accepted cookies.')
        except AssertionError:
            logger.warning('Cookies popup was not appeared.')

    def perform_search(self) -> None:
        """
        Perform the search operation on the AP News website using the search phrase.

        Returns:
        - None: Browser will be closed when elements are not found.
        """
        try:
            self.click_button_when_visible(self.SEARCH_BUTTON_LOCATOR)
            logger.info('Search Button Clicked')

            self.enter_text_when_visible_and_submit(self.SEARCH_INPUT_LOCATOR, self.search_phrase)
            logger.info('Wrote text in input and pressed Enter')

        except AssertionError as e:
            logger.warning(f'search execution failed due to {e}')
            raise AssertionError

    def select_category_filter(self) -> None:
        """
        Select the category filter for the search results.
        """

        try:
            self.click_element_when_visible(self.RESULT_FILTER_LOCATOR)
            logger.info('Category Clicked')

            self.click_button_when_visible(self.SEE_ALL_LOCATOR)
            logger.info('See All Clicked')

            self.click_element_when_visible(self.CATEGORY_SELECTION_LOCATOR.format(self.category))
            logger.info('Category Selected')

            self.browser.reload_page()
            logger.info('Page reloaded')
        except AssertionError as e:
            logger.warning(f'Category selection failed due to {e}')

    def select_sort_by(self) -> None:
        """
        Select the sort order for the search results.
        """
        try:
            self.select_from_list_by_value_when_visible(
                self.RESULT_FILTER_LOCATOR,
                self.SORT_BY_LOCATOR,
                self.SORT_BY_VALUE_LOCATOR
            )
            logger.info('Selected Newest in Sort By Dropdown')

            self.browser.reload_page()
            logger.info('Page reloaded')
        except AssertionError as e:
            logger.warning(f'Sort by selection failed due to {e}')

    def get_title_or_description(self, element: WebElement, locator: str) -> str | None:
        """
        Get the title or description from a web element.

        Args:
        - element: The web element to extract the title or description from.
        - locator (str): The locator for the title or description element.

        Returns:
        - str: The extracted title or description text.
        """
        try:
            elem = element.find_element(By.XPATH, locator)
            return self.get_element_text(elem)
        except NoSuchElementException:
            return None

    def get_date(self, element: WebElement) -> tuple:
        """
        Get the date from a web element.

        Args:
        - element: The web element to extract the date from.

        Returns:
        - tuple: The extracted date and a boolean indicating if the date limit is reached.
        """
        try:
            date_element = element.find_element(By.XPATH, self.DATE_NOW_LOCATOR)
        except (StaleElementReferenceException, NoSuchElementException):
            try:
                date_element = element.find_element(By.XPATH, self.DATE_LOCATOR)
            except NoSuchElementException:
                date_element = None

        if not date_element:
            return None, False

        news_date = self.get_element_text(date_element)
        news_date = parse_date(news_date)
        date_limit_reached = reached_date_limit(self.till_date, news_date)
        return news_date, date_limit_reached

    def get_image(self, element: WebElement) -> str | None:
        """
        Get the image URL from a web element.

        Args:
        - element: The web element to extract the image URL from.

        Returns:
        - str: The extracted image URL.
        """
        try:
            image_element = element.find_element(By.XPATH, self.IMAGE_LOCATOR)
        except NoSuchElementException:
            return None
        return self.get_image_attribute(image_element, "src")

    def process_elements(self, elements: list[WebElement]) -> bool:
        """
        Process each element in the list of elements to extract news details.

        Args:
        - elements: The list of web elements representing news articles.

        Returns:
        - bool: A boolean indicating if the date limit has been reached.
        """
        date_limit_reached = False
        for element_index, element in enumerate(elements, start=1):
            title = self.get_title_or_description(element, self.TITLE_LOCATOR)
            description = self.get_title_or_description(element, self.DESCRIPTION_LOCATOR)
            news_date, date_limit_reached = self.get_date(element)
            image_url = self.get_image(element)
            if date_limit_reached:
                break
            self.news_count += 1
            self.results.append(
                APNewsItem(
                    id=self.news_count,
                    title=title,
                    description=description,
                    date=news_date,
                    image=image_url,
                    search_phrase=self.search_phrase,
                    image_name=None
                )
            )

        return date_limit_reached

    def get_last_page_value(self) -> int:
        """
        Get the value of the last page in the pagination.

        Returns:
        - int: The value of the last page.
        """
        try:
            pagination_element = self.find_element_when_visible(self.PAGE_COUNT_LOCATOR, timeout=30)
            pagination = self.browser.get_text(pagination_element)
            last_page_value = pagination.split(' ')[-1]
            return int(last_page_value.replace(',', ''))
        except AssertionError as e:
            logger.warning(f"couldn't get pagination due to {e}")
        return 1

    def get_news_details(self) -> None:
        """
        Iterate through the pages and extract news details.

        This method will:
        - Get the total number of pages from the pagination element.
        - Iterate through each page, extract news details, and process them.
        - Check if the date limit is reached for any news article and stop the iteration if it is.
        - Log each significant step of the process.

        The iteration stops if:
        - The date limit is reached, or
        - The last page is processed.
        """
        last_page = self.get_last_page_value() + 1
        for index in range(2, last_page):
            try:
                self.wait_until_page_does_not_contain_element(self.RESULTS_LOCATOR, timeout=30)
                logger.info('Waited until page does not contain results element')
            except AssertionError:
                logger.warning('Results element did not disappear in 30 seconds')

            news_elements = self.find_elements_when_visible(self.RESULTS_LOCATOR, timeout=30)
            date_limit_reached = self.process_elements(news_elements)
            logger.info('Element processed')

            if date_limit_reached:
                logger.info('Reached to date limit')
                break

            self.click_element_when_visible(self.NEXT_PAGE_LOCATOR)
            logger.info(f'Clicked on next page {index}')

    def execute_process(self) -> None:
        """
        Execute the process to extract news articles from the AP News website.
        """
        logger.info('Process Execution started.')
        self.open_browser(self.base_url, True)
        logger.info('Browser opened')

        logger.info('Closing popup by cross.')
        self.close_donation_popup_by_cross()

        logger.info('Accepting cookies.')
        self.accept_cookies()

        logger.info('Searching news.')
        self.perform_search()

        logger.info('Selecting category.')
        self.select_category_filter()

        logger.info('Selecting newest filter.')
        self.select_sort_by()

        logger.info('Scrapping articles.')
        self.get_news_details()
        logger.info('Articles scrapped')

        logger.info('Closing Browser after getting articles.')
        self.close_browser()
        logger.info('Browser closed after getting articles.')

        logger.info('Downloading images from results.')
        self.download_images()
        logger.info('Downloading images from results.')

        logger.info('Writing results into excel.')
        self.write_items_to_excel()
        logger.info('Wrote results into excel.')

    def download_images(self, file_name: str = 'APNews_images') -> None:
        """
        Download images from the extracted news items.

        Args:
        - file_name (str): The directory to save the downloaded images.
        """
        output_dir = f'{self.output_dir}/{file_name}'
        os.makedirs(output_dir, exist_ok=True)
        for instance in self.results:
            instance.image_name = download_by_image_url(output_dir, instance.image)
        logger.info('Images download Completed')
        make_archive(output_dir, output_dir)
        logger.info('Archived Images Completed')

    def write_items_to_excel(
            self, file_name: str = "extracted_data.xlsx", sheet_name: str = "Extracted Data"
    ) -> None:
        """
        Write the extracted news items to an Excel file.

        Args:
        - file_name (str): The path to save the Excel file.
        - sheet_name (str): The name of the worksheet in the Excel file.
        """
        self.excel.create_workbook(f'{self.output_dir}/{file_name}')
        self.excel.create_worksheet(sheet_name)
        headers = [
            "Title",
            "Description",
            "date",
            "Image Name",
            "Contains Money",
            "Phrase Count"
        ]
        self.excel.append_rows_to_worksheet([headers], name=sheet_name)

        rows = []
        for instance in self.results:
            rows.append([
                instance.title,
                instance.description,
                instance.date,
                instance.image_name,
                instance.containing_amount,
                instance.count_of_search_phrase
            ])

        self.excel.append_rows_to_worksheet(rows, name=sheet_name)
        self.excel.save_workbook()
        logger.info('Execution Completed')
