
import sys
from TuringMachine import TuringMachine

class TuringMachineVerbose(TuringMachine):
    def __init__(self,
                 config_behav_table, # mapping from "configuration" to "behaviour"
                 initial_m_config = 'b',
                 initial_tape = {},
                 ):
        self._debug = False
        self._stop_each_step = True

        TuringMachine.__init__(
            self,
            config_behav_table,
            initial_m_config,
            initial_tape,
            )
    def setDebug(self, boolean):
        self._debug = boolean
        return True
    def setPromptEachStep(self, boolean):
        self._prompt_each_step = boolean
        return True

    def process(self,):
        res = TuringMachine.process(self)
        if self._prompt_each_step:
            res = self._prompt()
        return res

    def _prompt(self,):
        sys.stderr.write("continue? (y/n) \n")
        line = sys.stdin.readline().rstrip()
        if line in ("y", ""):
            sys.stderr.write("OK, proceeding to next step...\n")
            return True
        else:
            sys.stderr.write("OK, exiting...\n\n")
            return False

    def P0(self,):
        if self._debug: sys.stderr.write("...executing P0\n")
        return TuringMachine.P0(self)
    def P1(self,):
        if self._debug: sys.stderr.write("...executing P1\n")
        return TuringMachine.P1(self)
    def R(self,):
        if self._debug: sys.stderr.write("...executing R\n")
        return TuringMachine.R(self)
    def L(self,):
        if self._debug: sys.stderr.write("...executing L")
        return TuringMachine.L(self)

# prints 1/3 in binary
def print_one_third():
    cb_table = {
        # m-config: {scanned_symbol: (list_of_operations, next_m-config)
        "b": {None: (["P0","R"], "c")},
        "c": {None: (["R"],      "e")},
        "e": {None: (["P1","R"], "k")},
        "k": {None: (["R"],      "b")},
    }
    process(cb_table, "b", {})
    return
# prints 1/4 in binary
def print_one_fourth():
    cb_table = {
        # m-config: {scanned_symbol: (list_of_operations, next_m-config)
        "b": {None: (["P0","R"], "c")},
        "c": {None: (["R"],      "d")},
        "d": {None: (["P1","R"], "e")},
        "e": {None: (["R"],      "f")},
        "f": {None: (["P0","R"], "e")},
    }
    process(cb_table, "b", {})
    return

def process(cb_table, initial_m_config, initial_tape):
    TMV = TuringMachineVerbose(cb_table,
        initial_m_config,
        initial_tape)
    # set debug options
    #TMV.setDebug(True)
    TMV.setPromptEachStep(True)
    res = True
    while res == True:
        res = TMV.process()

def main():
    print_one_fourth()
    print_one_third()

if __name__ == '__main__':
    main()
