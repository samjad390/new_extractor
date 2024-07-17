class ApNewsLocators:
    """
    A class for storing XPath locators for elements on the AP News website.

    Attributes:
        DONATION_POP_CROSS_LOCATOR (str): Locator for the close button on the donation popup.
        DONATION_POP_DECLINE_LOCATOR (str): Locator for the decline button on the donation popup.
        SEARCH_BUTTON_LOCATOR (str): Locator for the search button on the search overlay.
        SEARCH_INPUT_LOCATOR (str): Locator for the search input field.
        RESULT_FILTER_LOCATOR (str): Locator for the result filter heading.
        SEE_ALL_LOCATOR (str): Locator for the "See All" button in the search filters.
        CHECKBOX_LOCATOR (str): Locator for the search filter checkbox.
        CATEGORY_SELECTION_LOCATOR (str): Locator for category selection using a text pattern.
        SORT_BY_LOCATOR (str): Locator for the sort by dropdown.
        SORT_BY_VALUE_LOCATOR (str): Value to select from the sort by dropdown.
        RESULTS_LOCATOR (str): Locator for the search results items.
        TITLE_LOCATOR (str): Locator for the title of a search result item.
        DESCRIPTION_LOCATOR (str): Locator for the description of a search result item.
        DATE_NOW_LOCATOR (str): Locator for the "now" timestamp in a search result item.
        DATE_LOCATOR (str): Locator for the date timestamp in a search result item.
        IMAGE_LOCATOR (str): Locator for the image in a search result item.
        PAGE_COUNT_LOCATOR (str): Locator for the pagination page count.
    """

    # Locator for the close button on the donation popup
    DONATION_POP_CROSS_LOCATOR = '//a[@title="Close"]'
    COOKIES_LOCATOR = '//*[contains(text(), "I Accept")]'

    # Locator for the decline button on the donation popup
    DONATION_POP_DECLINE_LOCATOR = '//div[@class="lb-declinewrap"]/a'

    # Locator for the search button on the search overlay
    SEARCH_BUTTON_LOCATOR = '//button[@class="SearchOverlay-search-button"]'

    # Locator for the search input field
    SEARCH_INPUT_LOCATOR = '//form[@class="SearchOverlay-search-form"]/label/input'

    # Locator for the result filter heading
    RESULT_FILTER_LOCATOR = '//div[@class="SearchFilter-heading"]'

    # Locator for the "See All" button in the search filters
    SEE_ALL_LOCATOR = '//button[@class= "SearchFilter-seeAll-button"]'

    # Locator for the search filter checkbox
    CHECKBOX_LOCATOR = '//div[@class="SearchFilterInput"]'

    # Locator for category selection using a text pattern
    CATEGORY_SELECTION_LOCATOR = "//*[contains(text(), '{}')]"

    # Locator for the sort by dropdown
    SORT_BY_LOCATOR = '//select[@name="s"]'

    # Value to select from the sort by dropdown
    SORT_BY_VALUE_LOCATOR = "3"

    # Locator for the search results items
    RESULTS_LOCATOR = '//div[@class="PageList-items"]/div[@class="PageList-items-item"]'

    # Locator for the title of a search result item
    TITLE_LOCATOR = './/div[@class="PagePromo-title"]/a[@class="Link "]/span'

    # Locator for the description of a search result item
    DESCRIPTION_LOCATOR = './/div[@class="PagePromo-description"]/a[@class="Link "]/span'

    # Locator for the "now" timestamp in a search result item
    DATE_NOW_LOCATOR = './/span[@class="Timestamp-template-now"]'

    # Locator for the date timestamp in a search result item
    DATE_LOCATOR = './/span[@class="Timestamp-template"]'

    # Locator for the image in a search result item
    IMAGE_LOCATOR = './/div[@class="PagePromo-media"]/a/picture/img'

    # Locator for the pagination page count
    PAGE_COUNT_LOCATOR = '//div[@class="Pagination-pageCounts"]'

    # Locator for the next page button in the pagination controls
    NEXT_PAGE_LOCATOR = '//div[@class="Pagination-nextPage"]'

    # Locator for No Result Found
    NO_RESULT_FOUND = '//div[@class="SearchResultsModule-noResults"]'
