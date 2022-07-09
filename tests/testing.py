import sys
from time import sleep

class TestRoutine:
    def __init__(self, use_execution_args=False,
                mandatory_args=0, interrupt_routine=None,
                repeat_interval=3):
        if use_execution_args and len(sys.argv) < mandatory_args + 1:
            raise Exception(f'This test requires at least {mandatory_args} arguments')
        self.use_execution_args = use_execution_args
        self.interrupt = interrupt_routine
        self.interval = repeat_interval

    def __call__(self, func):
        def test(*args, **kwargs):
            print('Starting test...')
            try:
                while True:
                    func(*args, **kwargs) if not self.use_execution_args else func(sys.argv[1:])
                    if self.interval < 1: break
                    for ii in range(self.interval):
                        print('\rRestarting in %s... (Cnrtl+C to stop)'%(self.interval -ii), end='')
                        sleep(1)
                    print('\rRestarting...' + ' ' * 5)
            except KeyboardInterrupt:
                print('\n\nTest ended manually...')
                if self.interrupt: self.interrupt()
            except Exception:
                print(Exception)
        return test
