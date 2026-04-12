from app.modules.calculations.functions import load_functions

FUNCTIONS = {}


def register(name):
    def wrapper(func):
        FUNCTIONS[name] = func
        return func

    return wrapper


def get(name):
    return FUNCTIONS[name]


load_functions()
