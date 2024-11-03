from functools import wraps

url_registry = {}

def document_url(description):
    def decorator(view_func):
        url_registry[view_func.__name__] = description
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            return view_func(*args, **kwargs)
        return wrapper
    return decorator