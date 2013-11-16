
import sys
import os.path
from TuringMachine import TuringMachine

class TuringMachineVerbose(TuringMachine):
    def __init__(self,
                 cb_table_filepath, # mapping from "configuration" to "behaviour"
                 initial_m_config = 'b',
                 initial_tape = {},
                 ):
        self._debug = False
        self._prompt_each_step = True

        TuringMachine.__init__(
            self,
            cb_table_filepath,
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

def process(cb_table_filepath, initial_m_config, initial_tape):
    TMV = TuringMachineVerbose(cb_table_filepath,
                               initial_m_config, initial_tape)
    # set debug options
    #TMV.setDebug(True)
    TMV.setPromptEachStep(True)
    res = True
    while res == True:
        res = TMV.process()

def main():
    cb_table_dir = "../cb_table/"
    # prints 1/3 in binary
    process(os.path.join(cb_table_dir, "one_forth.txt"), "b", {})
    # prints 1/4 in binary
    process(os.path.join(cb_table_dir, "one_third.txt"), "b", {})

if __name__ == '__main__':
    main()
