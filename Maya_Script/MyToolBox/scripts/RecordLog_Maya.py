# -*- coding: UTF-8 -*-
from functools import wraps
import time

class RecordLog_Maya(object):
    
    def __call__(self, func):
        @wraps(func)
        def log(*args, **kwargs):
            AllLog = '%s\n' %time.strftime("%m-%d %H:%M:%S", time.localtime())
            AllLog = '%s%s func enter\n' %(AllLog, func.__name__)
            func(*args, **kwargs)
            AllLog = '%s%s func leave\n' %(AllLog, func.__name__)
            #return func(*args, **kwargs)
        return log