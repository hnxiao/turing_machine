<?php

require_once './TuringMachine.php';

class TuringMachineVerbose extends TuringMachine
{
    protected $_debug = false;
    protected $_prompt_each_step = true;

    public function __construct(
        $cb_table_filepath, # mapping from "configuration" to "behaviour"
        $initial_m_config = 'b',
        $initial_tape = array())
    {
        $this->_debug = false;
        $this->_prompt_each_step = true;
        parent::__construct($cb_table_filepath, $initial_m_config, $initial_tape);
    }
    public function setDebug($boolean)
    {
        $this->_debug = $boolean;
        return true;
    }
    public function setPromptEachStep($boolean)
    {
        $this->_prompt_each_step = $boolean;
        return true;
    }

    public function process()
    {
        $res = parent::process();
        if ($this->_prompt_each_step == true) {
            $res = $this->_prompt();
        }
        return $res;
    }

    private function _prompt()
    {
        fputs(STDOUT, "continue? (y/n) \n");
        $line = trim(fgets(STDIN));
        if ($line == "y" || $line == "") {
            fputs(STDERR, "OK, proceeding to next step...\n");
            return true;
        } else {
            fputs(STDERR, "OK, exiting...\n\n");
            return false;
        }
    }

    protected function P0()
    {
        if ($this->_debug == true) {
            fputs(STDERR, "...executing P0\n");
        }
        return parent::P0();
    }
    protected function P1()
    {
        if ($this->_debug == true) {
            fputs(STDERR, "...executing P1\n");
        }
        return parent::P1();
    }
    protected function R()
    {
        if ($this->_debug == true) {
            fputs(STDERR, "...executing R\n");
        }
        return parent::R();
    }
    protected function L()
    {
        if ($this->_debug == true) {
            fputs(STDERR, "...executing L\n");
        }
        return parent::L();
    }
}

function do_tmv_process($cb_table_filepath, $initial_m_config, $initial_tape)
{
    $tmv = new TuringMachineVerbose($cb_table_filepath, $initial_m_config, $initial_tape);
    # set debug options
    $tmv->setDebug(true);
    $tmv->setPromptEachStep(true);
    $res = true;
    while ($res == true) {
        $res = $tmv->process();
    }
}

$cb_table_dir = "../cb_table/";
# prints 1/3 in binary
do_tmv_process(sprintf("%s/one_forth.txt", $cb_table_dir), "b", array());
# prints 1/4 in binary
do_tmv_process(sprintf("%s/one_third.txt", $cb_table_dir), "b", array());

