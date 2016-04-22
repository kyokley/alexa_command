import os
from ouimeaux.environment import Environment
from ouimeaux.utils import matcher

SWITCH_NAME = 'mercury'
matches = matcher(SWITCH_NAME)

def main():
    # Forcing the machine to shutdown? What's the worst that can happen?
    os.system('shutdown -h now')

def start_up():
    env = Environment()
    env.start()
    env.discover(5)
    found = None
    for switch in env.list_switches():
        if matches(switch):
            found = env.get_switch(switch)
            break
    else:
        raise Exception('Switch not found!')

    found.off()
    env.wait(30)
    found.on()
