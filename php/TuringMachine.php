<?php

class TuringMachine
{
    protected $_cb_table = array();
    protected $_m_config = "b";
    protected $_tape = array();
    protected $_r = 0;

    public function __construct(
        $cb_table_filepath, // mapping from "configuration" to "behaviour"
        $initial_m_config = 'b',
        $initial_tape = array())
    {
        $this->_cb_table = $this->load_cb_table($cb_table_filepath);
        $this->_m_config = $initial_m_config;
        $this->_tape = $initial_tape;
        $this->_r = 0; // index of "scanned square"
        // TODO: use constant for symbols??
        return;
    }

    /*
     * main process
    */
    public function process()
    {
        // scan symbol on tape
        $scanned_symbol = $this->_scan_tape();
        // lookup table
        $lookup_results = $this->_lookup_table($scanned_symbol);
        $operations = $lookup_results[0];
        $next_m_config = $lookup_results[1];

        // operations
        foreach ($operations as $operation) {
            try {
                //fputs(STDERR, sprintf("executing $operation ...\n"));
                call_user_func(array($this, $operation));
            } catch (TuringMachineError $e) {
                return $this->_halt("calling operation functio failed.");
            }
        }
        $this->_m_config = $next_m_config;
        // TODO: make this output optional??
        $this->_output_current_tape();
        return true;
    }
    protected function _halt($message)
    {
        fputs(STDERR, "This machine stopped! $message\n");
        exit(1);
    }
    protected function _output_current_tape()
    {
        fputs(STDOUT, var_export(array_values($this->_tape)) . "\n");
        return true;
    }
    protected function _lookup_table($scanned_symbol)
    {
        if (array_key_exists($this->_m_config, $this->_cb_table)) {
            if (array_key_exists($scanned_symbol, $this->_cb_table[$this->_m_config])) {
                return $this->_cb_table[$this->_m_config][$scanned_symbol];
            }
        }
        return $this->_halt("lookup table failed.");
    }
    protected function _scan_tape()
    {
        if (array_key_exists($this->_r, $this->_tape)) {
            $scanned_symbol = $this->_tape[$this->_r];
        } else {
            $this->_tape[$this->_r] = "";
        }
        return $this->_tape[$this->_r];
    }

    /*
    * operations
    */
    protected function P0()
    {
        return $this->_print_to_tape(0);
    }
    protected function P1()
    {
        return $this->_print_to_tape(1);
    }
    protected function R()
    {
        $this->_r += 1;
        return true;
    }
    protected function L()
    {
        $this->_r -= 1;
        return true;
    }
    protected function _print_to_tape($symbol_to_print)
    {
        $this->_tape[$this->_r] = $symbol_to_print;
        return true;
    }

    protected function load_cb_table($filepath, $columns_sep="\t", $within_column_sep=",")
    {
        $cb_table = array();
        $file_handle = fopen($filepath, 'r');
        if ($file_handle === false) {
            return array();
        }
        while( ($line = fgets($file_handle)) !== false) {
            try {
                $line = rtrim($line);
                $columns = explode($columns_sep, $line);
                if (count($columns) != 4) {
                    fputs(STDERR, sprintf("Invalid input line: %s", $line));
                    exit(0);
                }
                $cb_table[$columns[0]] = array(
                    $columns[1] => array(
                        explode($within_column_sep, $columns[2]),
                        $columns[3]
                    )
                );
            } catch (Exception $e) {
                fputs(STDERR, sprintf("Invalid input line: %s", $line));
                exit(0);
            }
        }
        fclose($file_handle);
        return $cb_table;
    }
}

/*
function do_tm_process($cb_table_filepath, $initial_m_config, $initial_tape, $interval = 1.0)
{
    $tm = new TuringMachine($cb_table_filepath, $initial_m_config, $initial_tape);
    while (true) {
        sleep($interval);
        $res = $tm->process();
    }
}

$cb_table_dir = "../cb_table/";
# prints 1/3 in binary
#do_tm_process(sprintf("%s/one_forth.txt", $cb_table_dir), "b", array());
# prints 1/4 in binary
do_tm_process(sprintf("%s/one_third.txt", $cb_table_dir), "b", array());
*/

