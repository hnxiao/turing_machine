
import sys

class TuringMachine:
    def __init__(self,
                 config_behav_table, # mapping from "configuration" to "behaviour"
                 initial_m_config = 'b',
                 initial_tape = {},
                 ):
        self._cb_table = config_behav_table
        self._m_config = initial_m_config
        self._tape = initial_tape
        self._r = 0 # index of "scanned square"

        # TODO: define constant m-config
        return

    ################
    # main process #
    ################
    def process(self,):
        scanned_symbol = self._scan_tape()
        (operations, next_m_config) = self._lookup_table(scanned_symbol)
        for operation in operations:
            try:
                getattr(self, operation)()
            except AttributeError:
                self.halt()
        self._m_config = next_m_config
        # TODO: make this output optional?
        self._output_current_tape()
        return True
    def halt(self,):
        sys.stderr.write("This machine stopped!\n")
        exit(1)

    def _output_current_tape(self,):
        sys.stdout.write(self._tape.values())
        sys.stdout.write("\n")
        return True
    def _lookup_table(self, scanned_symbol):
        try:
            (operations, next_m_config) = self._cb_table[self._m_config][scanned_symbol]
        except IndexError:
            self.halt()
        return (operations, next_m_config)
    def _scan_tape(self,):
        try:
            scanned_symbol = self._tape[self._r]
        except KeyError:
            self._tape[self._r] = None
        return self._tape[self._r]

    ##############
    # behaviours #
    ##############
    def P0(self,):
        return self._print_to_tape(0)
    def P1(self,):
        return self._print_to_tape(1)
    def _print_to_tape(self, symbol_to_print):
        self._tape[self._r] = symbol_to_print
        return True
    def R(self,):
        self._r += 1
        return True
    def L(self,):
        self._r -= 1
        return True

