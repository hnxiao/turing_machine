
import sys
import os.path
import time

class TuringMachine:
    def __init__(self,
                 cb_table_filepath, # mapping from "configuration" to "behaviour"
                 initial_m_config = 'b',
                 initial_tape = {},
                 ):
        self._cb_table = self.load_cb_table(cb_table_filepath)
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
            self._tape[self._r] = ""
        return self._tape[self._r]

    ##############
    # operations #
    ##############
    def P0(self,):
        return self._print_to_tape(0)
    def P1(self,):
        return self._print_to_tape(1)
    def R(self,):
        self._r += 1
        return True
    def L(self,):
        self._r -= 1
        return True
    def _print_to_tape(self, symbol_to_print):
        self._tape[self._r] = symbol_to_print
        return True

    def load_cb_table(self, filepath,
                      columns_sep="\t", within_column_sep=","):
        cb_table = {}
        f = open(filepath)
        try:
            for line in f.readlines():
                columns = line.rstrip().split(columns_sep)
                if len(columns) != 4:
                    sys.stderr.write("Invalid input line: %s", line)
                    exit(0)
                cb_table[columns[0]] = {columns[1]:
                                        (columns[2].split(within_column_sep),
                                         columns[3])
                                        }
        except KeyError:
            sys.stderr.write("Invalid input line: %s", line)
            exit(0)
        finally:
            f.close()
        return cb_table


def process(cb_table_filepath, initial_m_config, initial_tape, interval=0.5):
    TMV = TuringMachine(cb_table_filepath,
                        initial_m_config, initial_tape)
    while True:
        time.sleep(interval)
        res = TMV.process()

def main():
    cb_table_dir = "../cb_table/"
    # prints 1/3 in binary
    #process(os.path.join(cb_table_dir, "one_forth.txt"), "b", {})
    # prints 1/4 in binary
    process(os.path.join(cb_table_dir, "one_third.txt"), "b", {})

if __name__ == '__main__':
    main()
