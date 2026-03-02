import sys

def FailOnCall():
    raise Exception('Kaboom!')

FailOnCall()