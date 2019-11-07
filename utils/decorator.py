from functools import wraps


def clean(function):
    @wraps(function)
    def decorated(self, *args, **kwargs):
        res = function(self, *args, **kwargs)
        if type(res) == str:
            return res.strip().replace('\n', '')
        elif type(res) == list:
            return [s.strip().replace('\n', '') for s in res]
        else:
            return res
    return decorated
