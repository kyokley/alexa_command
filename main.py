import os
import gevent
import time
from ouimeaux.environment import Environment
from ouimeaux.utils import matcher
from celery import Celery

SWITCH_NAME = 'mercury'
matches = matcher(SWITCH_NAME)

app = Celery('mercury_tasks', broker='amqp://guest@localhost//')

def main():
    # Forcing the machine to shutdown? What's the worst that can happen?
    os.system('shutdown -h now')

def get_switch():
    env = Environment()

    try:
        env.start()
    except:
        pass

    env.discover(5)
    found = None
    for switch in env.list_switches():
        if matches(switch):
            found = env.get_switch(switch)
            break
    else:
        raise Exception('Switch not found!')

    return found

def start_up():
    switch = get_switch()
    switch.off()
    _switch_on.delay()

@app.task
def _switch_on():
    switch = get_switch()
    time.sleep(3)
    switch.on()
