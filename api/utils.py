from time import time, sleep
from random import random


def random_wait(resp):
    # create random number to be used as waiting time in secs
    # between 0-3 secs
    sleep(random() * 3)
    return resp


def kitty_to_json(kitty):
    return {"id": kitty.id, "name": kitty.name}


def last_log():
    # returns the last message from the log file
    import os
    with open("kitties.log", "r") as logs:
        lines = logs.readlines()
    if lines:
        return lines[-2] if lines[-1] == "" else lines[-1]


def process_message(_message: bytes):
    message = _message.decode("utf-8")
    method, resp_time, timestamp = message.split(",")
    return method, int(resp_time), int(timestamp)
