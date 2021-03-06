from start_up import start_up
import fauxmo
import time
import requests
from settings import MERCURY_HOST, MERCURY_PORT
from datetime import datetime

from debounce_handler import debounce_handler


def log(message):
    print('%s: %s' % (datetime.now().strftime('%d-%b-%Y %H:%M'),
                      message))


class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"mercury": 52001}

    def act(self, client_address, state):
        try:
            if state:
                log('Got message to send start up')
                start_up()
            else:
                # Send POST to mercury to kick off shutdown
                log('Got message to send shutdown to %(host)s:%(port)s'
                    % {'host': MERCURY_HOST,
                       'port': MERCURY_PORT})
                resp = requests.post(
                    'http://%(host)s:%(port)s/mercury'
                    % {'host': MERCURY_HOST,
                       'port': MERCURY_PORT}, timeout=1)
                resp.raise_for_status()
        except Exception as e:
            log(str(e))
        log("State %s from client @ %s" % (state, client_address))
        return True


if __name__ == "__main__":
    # Startup the fauxmo server
    log("Starting up")
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    log("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            log("Critical exception: " + str(e))
            break
