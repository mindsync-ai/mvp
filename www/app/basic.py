def is_get(method):
    return method == "GET"

def is_post(method):
    return method == "POST"

def is_logged_in(session):
    return "user" in session
