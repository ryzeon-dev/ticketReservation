import requests
import sys


import python.lib as lib

URL = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    print(lib.updateReservation(
        'bgDYN9E5aVp4na4ohaZAsWAgM9CCI3M1p80JdQ9HPNsmMcPsoZdCU9jW7JmgyrqQ',
        '1', '10', '1783298406992867'
    ))