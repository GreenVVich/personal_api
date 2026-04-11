FUNCTIONS = {}

def register(name):
    def wrapper(func):
        FUNCTIONS[name] = func
        return func
    return wrapper

def get(name):
    return FUNCTIONS[name]

from app.modules.calculations.functions import load_functions

load_functions()
