import os
import time
from ouimeaux.environment import Environment
from ouimeaux.utils import matcher
from celery import Celery

SWITCH_NAME = 'mercury'
matches = matcher(SWITCH_NAME)

mercury_task = Celery('mercury_tasks', backend='redis://localhost', broker='amqp://guest@localhost//')

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

@mercury_task.task
def _switch_on():
    print "Getting switch"
    switch = get_switch()
    time.sleep(30)
    print "Activating switch"
    switch.on()

def start_up():
    switch = get_switch()
    switch.off()
    print "Making async call"
    _switch_on.delay()
    _switch_on.delay()
