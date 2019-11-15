from functools import wraps


def clean(function):
    @wraps(function)
    def decorated(self, *args, **kwargs):
        try:
            res = function(self, *args, **kwargs)
        except Exception as e:
            return None
        if type(res) == str:
            return res.strip().replace('\n', '')
        elif type(res) == list:
            return [s.strip().replace('\n', '') for s in res]
        elif type(res) == dict:
            return {s.strip().replace('\n', ''): res[s].strip().replace('\n', '') for s in res}
        else:
            return res
    return decorated
