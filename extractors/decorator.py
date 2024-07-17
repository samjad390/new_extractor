import time
import uuid

from logging_config import logger


def retry(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):

            error = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error = e
                    logger.info(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            self = args[0]
            browser = getattr(self, "browser", None)
            if browser:
                browser.capture_page_screenshot(f"{self.output_dir}/{uuid.uuid4().hex}.png")
            raise Exception(error)

        return wrapper

    return decorator
