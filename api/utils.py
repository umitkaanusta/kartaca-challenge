from time import sleep
from random import random


def random_wait(resp):
    # create random number to be used as waiting time in secs
    # between 0-3 secs
    sleep(random() * 3)
    return resp


def kitty_to_json(kitty):
    return {"id": kitty.id, "name": kitty.name}
