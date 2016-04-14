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
        if not hasattr(current_user,'banned'):
            user = current_user._get_current_object()
            user.banned = False
            current_app.dbbackend.save(user)
        if current_user.is_banned:
            return redirect("/")
        else:
            return f(*args, **kwargs)
    return wrapper
