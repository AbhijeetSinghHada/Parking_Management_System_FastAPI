import logging
import functools


def setup_logger(level=logging.DEBUG, filename='log.txt'):

    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s:%(lineno)s %(levelname)s:%(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        filename=filename
                        )


def log(logger):
    def log_operation(fun):

        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            operation = fun.__name__
            args_repr = [repr(item) for item in args[1:]]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            val = fun(*args, **kwargs)
            logger.debug(
                f"{operation}  called with params : {signature} returned : {val}.\n")
            return val
        return wrapper
    return log_operation
