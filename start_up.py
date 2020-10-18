import time
from ouimeaux.environment import Environment
from ouimeaux.utils import matcher
from celery import Celery
from settings import CELERY_VHOST

SWITCH_NAME = 'Real mercury outlet'
matches = matcher(SWITCH_NAME)

mercury_task = Celery('start_up',
                      backend='redis://localhost',
                      broker='amqp://guest@localhost/%s' % CELERY_VHOST)


def get_switch():
    env = Environment()

    try:
        env.start()
    except Exception:
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
    print("Getting switch")
    switch = get_switch()
    time.sleep(30)
    print("Activating switch")
    switch.on()


def start_up():
    switch = get_switch()
    switch.off()
    print("Making async call")
    _switch_on.delay()


if __name__ == '__main__':
    start_up()
