import random

import time


def create_ticket():
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    ticket = ''
    for i in range(15):
        ticket += random.choice(s)
    now_time = int(time.time())
    ticket += str(now_time)
    return ticket