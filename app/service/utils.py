import logging
from functools import wraps


def func_logger():

    def inner(func):

        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                logging.info(f'{func.__module__}.{func.__name__}: completed successfuly.')
                return result
            except Exception as e:
                if len(e.args):
                    description = e.args[0]
                else:
                    description = e.__getattribute__('detail')
                logging.error(f'{func.__module__}.{func.__name__}: {description}')
                raise e
        return wrapped
    return inner
