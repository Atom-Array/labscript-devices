from labscript import (
    PseudoclockDevice,
    Pseudoclock,
    LabscriptError
)


class NIStreamBlaster(PseudoclockDevice):
    description = "NIStreamBlaster"
    clock_limit = 10e6  # Maximum sample clock rate
    clock_resolution = 1/clock_limit  # time granularity

    def __init__(self, name, nimax_name, samp_rate=10e6, trigger_device=None, trigger_connection=None):
        PseudoclockDevice.__init__(
            self=self,
            name=name,
            trigger_device=trigger_device,
            trigger_connection=trigger_connection
        )

        # Parameter sanity checks
        if samp_rate > self.clock_limit:
            raise LabscriptError(
                f'The maximum sample rater NIStreamBlaster supports is {self.clock_limit * 1e-6:.2f} MHz.'
                f'The requested rate of {samp_rate * 1e-6:.2f} MHz is above the limit'
            )

        self.BLACS_connection = nimax_name
        self.pseudoclock = Pseudoclock(
            name=name + '_pseudoclock',
            pseudoclock_device=self,
            connection='pseudoclock'
        )

    def generate_code(self, hdf5_file):
        PseudoclockDevice.generate_code(self=self, hdf5_file=hdf5_file)

        group = self.init_device_group(hdf5_file)

        print(self.pseudoclock.clock)
