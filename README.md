# SipHash
![verify](https://github.com/hydroid7/siphash/actions/workflows/verify.yml/badge.svg)

Siphash is a fast and simple hashing algorithm. This repository presents an implementation in Verilog tested with Cocotb testbenches.
[Cocotb](https://github.com/cocotb/cocotb) is an open-source python-based alternative to SystemVerilog testbenches. Since python is a productive high-level language with a rich ecosystem of well-maintained libraries such as numpy, tensorflow and pytorch, using python for verification allows the direct usage of those libraries. Cocotb does not simulate the testbench itself. Instead, it interfaces with the simulator.

# Microcode
The high level module implements an interface that is controlled with microcode operations. Each opcode is 68 bit wide.
It is simply constructed from 4 bit long prefix and a 64 bit long data.

|Opcode | Meaning|
|-------|--------|
|`0000`  | Set first half of key|
|`0001`  | Set second half of key|
|`0010`  | Compression round with data|
|`0011`  | Finalize|

All other opcodes are for future use, like the change of compression and finalization rounds.
The module can accept an opcode each cycle. However, take into account, that the finalization takes more than one clock cycle depending on the round configuration.

## Setup

The project uses `Makefile`s to make the python virtual environment and run tests.
So for making the environment run:
```
make pyenv
```

## Tests & Lints

You can run tests with `make test` and code linting with Verilator `make lint`. To qualify you code for the coding standards of this repository, your code should pass both checks.

## View Waveforms

Waveforms are generated in when the tests are executed. View them with `gtkwave`:
```bash
$ gtkwave siphash/tests/siphash.vcd
```
