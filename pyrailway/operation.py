class Operation:
    def __init__(self, *stations):
        self.stations = stations
        
        
    def __call__(self, params=None, **dependencies):
        options = dict(params=(params or {}), **dependencies)
        success = True
        for station in self.stations:
            if (success and station.runs_on_success) or (not success and station.runs_on_failure): 
                success = station(options, dependencies)
                if success == FailFast:
                    return Result(False, options)
            
        return Result(success, options)


class Result:
    def __init__(self, success, result_data):
        self.result_data = result_data
        self.success = success
        
    @property
    def failure(self):
        return not self.success
    
    def __getitem__(self, key):
        return self.result_data[key]
    
    def __contains__(self, key):
        return key in self.result_data
    
    def get(self, key):
        return self.result_data.get(key)
    
    
    
class FailFast:
    pass


class Activity:
    
    runs_on_success = False
    runs_on_failure = False
    
    def __init__(self, func):
        self.func = func
        
    def callfunc(self, options, dependencies):
        params = options["params"]
        return self.func(options=options, params=params, **dependencies)
    
    def __call__(self, options, dependencies):
        self.callfunc(options, dependencies)
        return True

    def __repr__(self):
        return "{} with {}".format(self.__class__.__name__, self.func.__name__)
    

class step(Activity):
    
    runs_on_success = True

    def __init__(self, func, fail_fast=False):
        self.func = func
        self.fail_fast = fail_fast

    def __call__(self, options, dependencies):
        res = self.callfunc(options, dependencies)
        success = bool(res)
        if not success and self.fail_fast:
            return FailFast
        return success


class failure(Activity):

    runs_on_failure = True
    
    def __call__(self, options, dependencies):
        self.callfunc(options, dependencies)
        return False
        

class success(Activity):

    runs_on_success = True
