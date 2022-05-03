import sys
import os

from mydreamz.mydreamz import MyDreamz

def validate_args(arg):
    """
    """
    if len(arg) == 1:
        return "127.0.0.1:10001"
    elif len(arg) > 1:
        ip_port = arg[1]
        return ip_port



if __name__ == '__main__':
    arg = sys.argv

    ip_port = validate_args(arg)

    obj = MyDreamz()
    obj.initialize(ip_port)
    obj.run()

