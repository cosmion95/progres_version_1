from django.db import connection
import sys


class HandledCursor:
    def __init__(self):
        self.cursor = connection.cursor()

    def callproc(self, proc_name, parameters):
        self.cursor.callproc(proc_name, parameters)

    def callfunc(self, func_name, return_type, parameters):
        function_return_value = self.cursor.callfunc(func_name, return_type, parameters)
        return function_return_value
