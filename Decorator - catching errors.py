def catch_errors(func):
    def inner(*args):
        try:
            func(*args)
        except AssertionError:
            logging.error(f"{func} assertion error, something went wrong", exc_info=True)
    return inner

# then use @catch_errors on func