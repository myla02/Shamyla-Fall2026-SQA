import logging
import time
from functools import wraps

logging.basicConfig(
    filename="forensics.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def forensic_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start

            logging.info(
                "%s | SUCCESS | %.6f seconds",
                func.__name__,
                duration
            )
            return result

        except Exception as error:
            duration = time.perf_counter() - start

            logging.error(
                "%s | ERROR: %s | %.6f seconds",
                func.__name__,
                type(error).__name__,
                duration
            )
            raise

    return wrapper