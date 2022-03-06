def api_key_required(decorated_method):
    def wrapper(*args, **kwargs):
        for i in request.headers:
            if i[0] == 'API_KEY' and i[1] == API_KEY:
                return decorated_method(*args, **kwargs)
        else:
            return {'error':'valid API key missing!'}, 401
    return wrapper
