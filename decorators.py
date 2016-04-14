from flask.ext.login import current_user
from flask import redirect
from functools import wraps
def user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect("/login")
        else:
            return f(*args, **kwargs)
    return wrapper
def not_banned(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if(current_user.banned == None):
            current_user.banned = False
        if current_user.is_banned:
            return redirect("/")
        else:
            return f(*args, **kwargs)
    return wrapper
