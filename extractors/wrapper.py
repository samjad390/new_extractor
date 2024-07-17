from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class BrowserWrapper:
    """
    A wrapper class for Selenium browser operations and Excel file manipulations using RPA Framework.

    Attributes:
        browser (Selenium): An instance of the Selenium library for browser automation.
        excel (Files): An instance of the Files library for handling Excel files.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the BrowserWrapper with optional Selenium keyword arguments.

        Args:
            **kwargs: Optional keyword arguments to configure the Selenium browser instance.
        """
        self.browser = Selenium(**kwargs)
        self.excel = Files()

    def open_browser(self, url: str, maximize: bool = False) -> None:
        """
        Opens a browser and navigates to the specified URL.

        Args:
            url (str): The URL to open in the browser.
            maximize (bool): Whether to maximize the browser window. Default is False.
        """
        self.browser.open_available_browser(
            url, maximized=maximize
        )

    def get_element_text(self, element: WebElement) -> str:
        """
        Retrieves the text content of a specified web element.

        Args:
            element: The web element from which to retrieve the text.

        Returns:
            str: The text content of the web element.
        """
        return self.browser.get_text(element)

    def click_button_when_visible(self, locator: str, timeout: int = 10) -> None:
        """
        Waits until a button is visible and then clicks it.

        Args:
            locator (str): The locator of the button element.
            timeout (int): The maximum time to wait for the element to be visible. Default is 10 seconds.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        self.browser.click_button(locator)

    def click_element_when_visible(self, locator: str, timeout: int = 10) -> None:
        """
        Waits until an element is visible and then clicks it.

        Args:
            locator (str): The locator of the element.
            timeout (int): The maximum time to wait for the element to be visible. Default is 10 seconds.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        self.browser.click_element(locator)

    def find_element_when_visible(
            self, locator: str, element: WebElement | None = None, timeout: int = 10
    ) -> WebElement:
        """
        Waits until an element is visible and then finds it.

        Args:
            locator (str): The locator of the element to find.
            element: The parent element to search within. Default is None.
            timeout (int): The maximum time to wait for the element to be visible. Default is 10 seconds.

        Returns:
            WebElement: The found web element.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        return self.browser.find_element(locator, parent=element)

    def find_elements_when_visible(self, locator: str, timeout: int = 10) -> list[WebElement]:
        """
        Waits until elements are visible and then finds them.

        Args:
            locator (str): The locator of the elements to find.
            timeout (int): The maximum time to wait for the elements to be visible. Default is 10 seconds.

        Returns:
            list: A list of found web elements.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        return self.browser.find_elements(locator)

    def get_image_attribute(self, element: WebElement, attribute: str) -> str:
        """
        Retrieves a specified attribute value from an image element.

        Args:
            element: The image element.
            attribute (str): The name of the attribute to retrieve.

        Returns:
            str: The value of the specified attribute.
        """
        return self.browser.get_element_attribute(element, attribute)

    def wait_for_element_visible(self, locator: str, timeout: int = 10) -> None:
        """
        Waits until a specified element is visible.

        Args:
            locator (str): The locator of the element.
            timeout (int): The maximum time to wait for the element to be visible. Default is 10 seconds.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)

    def does_page_contain_element(self, locator: str) -> bool:
        """
        Waits until a specified element is visible.

        Args:
            locator (str): The locator of the element.

        Returns:
            bool: It will return True if the page is containing element otherwise False.
        """
        return self.browser.does_page_contain_element(locator)

    def wait_until_page_does_not_contain_element(self, locator: str, timeout: int = 10) -> None:
        """
        Waits until a specified element is no longer present on the page.

        Args:
            locator (str): The locator of the element.
            timeout (int): The maximum time to wait for the element to be absent. Default is 10 seconds.
        """
        self.browser.wait_until_page_does_not_contain_element(locator, timeout=timeout)

    def enter_text_when_visible_and_submit(self, locator: str, text: str, timeout: int = 10) -> None:
        """
        Waits until an element is visible, enters text into it, and submits the form.

        Args:
            locator (str): The locator of the element.
            text (str): The text to enter into the element.
            timeout (int): The maximum time to wait for the element to be visible. Default is 10 seconds.
        """
        self.browser.wait_until_element_is_visible(locator, timeout=timeout)
        self.browser.input_text(locator, text)
        self.browser.press_keys(locator, Keys.ENTER)

    def select_from_list_by_value_when_visible(
            self, wait_locator: str, select_locator: str, value: str
    ) -> None:
        """
        Waits until a list element is visible and selects an option by value.

        Args:
            wait_locator (str): The locator of the element to wait for.
            select_locator (str): The locator of the list element.
            value (str): The value of the option to select.
        """
        self.browser.wait_until_element_is_visible(wait_locator)
        self.browser.select_from_list_by_value(select_locator, value)

    def close_browser(self) -> None:
        """
        Close browser.
        """
        self.browser.close_browser()
