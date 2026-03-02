import sys

def FailOnCall():
    print('This is about to fail!')
    sys.exit(1)

FailOnCall()