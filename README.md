# AP News Extractor

This project is designed to extract news articles from the AP News website using web automation with Selenium and RPA Framework. It includes functionality to perform searches, filter results by category, sort results, and extract details such as titles, descriptions, dates, and images of the news articles. The extracted data is then saved into an Excel file.

## Features

- **Browser Automation**: Uses Selenium for browser automation to navigate and interact with the AP News website.
- **Excel File Manipulation**: Uses RPA Framework's Files library to handle Excel files for storing extracted data.
- **Search and Filter**: Performs search operations on the AP News website based on a search phrase and filters results by category.
- **Data Extraction**: Extracts news article details such as titles, descriptions, dates, and images.
- **Image Downloading**: Downloads images associated with the news articles and archives them.
- **Error Handling and Retry**: Implements retry mechanisms for robust error handling during the extraction process.
- **Logging**: Provides detailed logging for monitoring the execution process.

## Project Structure

- `wrapper.py`: Contains the `BrowserWrapper` class that wraps Selenium browser operations and Excel file manipulations.
- `apnews.py`: Contains the `ApNews` class that extends `BrowserWrapper` and includes methods for extracting news articles from the AP News website.
- `models.py`: Contains the `APNewsItem` model class representing a news item from the AP News site.
- `locators.py`: Contains the `ApNewsLocators` class with XPath locators for elements on the AP News website.
- `utils.py`: Contains utility functions for date handling, text processing, and image downloading.

## Requirements

- Python 3.x
- Selenium
- RPA Framework
- Pydantic
- Dateutil

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/apnews-extractor.git

2. Navigate into the project directory:
   ```bash
   cd apnews-extractor

3. Install the required packages:
   ```bash
   pip install -r requirements.txt


## Logging

This project utilizes logging to provide detailed information about the execution process. Logging is crucial for monitoring the automation process, debugging issues, and understanding the flow of execution. Here's how logging is implemented:

- **Logging Configuration**: Logging configuration is set up at the beginning of the script using Python's built-in logging module.
  
- **Log Levels**: Different log levels (e.g., DEBUG, INFO, WARNING, ERROR) are used to differentiate between informational messages and potential issues or errors.

- **Log Messages**: Throughout the execution process, relevant actions, errors, and important milestones are logged using appropriate log levels.

- **Log Files**: Logs are stored in a designated file (`apnews_extractor.log` by default) to maintain a record of execution history.

By reviewing the logs, you can gain insights into each step of the extraction process, identify any errors encountered, and track the overall progress of the automation.

