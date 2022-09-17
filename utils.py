import time


def retry(func, *args, exceptions=(Exception,), max_retry_count=-1, timeout=0):
    retries_left = max_retry_count
    while retries_left != 0:
        try:
            return func(*args)
        except exceptions as e:
            pass
        finally:
            retries_left -= 1
            time.sleep(timeout)
