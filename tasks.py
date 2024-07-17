import traceback

from robocorp.tasks import task

from config import RCCWortItems
from extractors.apnews import ApNews
from logging_config import logger


@task
def new_extraction_task():
    try:
        logger.info('Task Executed')
        work_item = RCCWortItems()
        logger.info('Initializing ApNews scrapper')
        ap_news = ApNews(
            search_phrase=work_item.search_phrase,
            no_of_months=work_item.no_of_months,
            category=work_item.category
        )
        ap_news.execute_process()
        logger.info('ApNews scrapper process completed.')
    except Exception as e:
        logger.error(f'ApNews scrapper execution failed due to {e}')
        traceback.print_exc()
    finally:
        logger.info('Extraction Task Completed...')

