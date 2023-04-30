# SipHash
![verify](https://github.com/hydroid7/siphash/actions/workflows/verify.yml/badge.svg)

Siphash is a fast and simple hashing algorithm. This repository presents an implementation in Verilog tested with Cocotb testbenches.
[Cocotb](https://github.com/cocotb/cocotb) is an open-source python-based alternative to SystemVerilog testbenches. Since python is a productive high-level language with a rich ecosystem of well-maintained libraries such as numpy, tensorflow and pytorch, using python for verification allows the direct usage of those libraries. Cocotb does not simulate the testbench itself. Instead, it interfaces with the simulator.


## Setup

The project uses `Makefile`s to make the python virtual environment and run tests.
So for making the environment run:
```
make pyenv
```

## Tests

You can run tests with `make test`.

## View Waveforms

Waveforms are generated in when the tests are executed. View them with `gtkwave`:
```bash
$ gtkwave siphash/tests/siphash.vcd
```
