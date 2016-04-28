import os

def shutdown():
    # Forcing the machine to shutdown? What's the worst that can happen?
    os.system('shutdown -h now')
