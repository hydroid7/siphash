# SipHash
![verify](https://github.com/hydroid7/siphash/actions/workflows/verify.yml/badge.svg)

Siphash is a fast and simple hashing algorithm. This repository presents an implementation in Verilog tested with Cocotb testbenches.
[Cocotb](https://github.com/cocotb/cocotb) is an open-source python-based alternative to SystemVerilog testbenches. Since python is a productive high-level language with a rich ecosystem of well-maintained libraries such as numpy, tensorflow and pytorch, using python for verification allows the direct usage of those libraries. Cocotb does not simulate the testbench itself. Instead, it interfaces with the simulator.

# Module Usage
The high level module implements a `microcode` based interface that is controlled with instructions. Each opcode is 68 bit wide.
It is simply constructed from 4 bit long prefix and a 64 bit long data.

|Opcode  |  Payload    | Meaning|
|--------|-------------|--------|
|`0000`  |`key[0:63]`  | Set first half of key|
|`0001`  |`key[64:127]`| Set second half of key|
|`0010`  | 64 bit `m`  | Compression round with data|
|`0011`  | unused      | Finalize|

All other opcodes are for future use, like the change of compression and finalization rounds.
The module can accept an opcode each cycle. However, take into account, that the finalization takes more than one clock cycle depending on the round configuration.

## Timing Diagram

<img src="https://svg.wavedrom.com/%7Bsignal%3A%20%5B%0A%20%20%7Bname%3A%20%27clk%27%2C%20wave%3A%20%27p.......%7C...%7C..%27%7D%2C%0A%20%20%5B%27Control%27%2C%0A%20%20%09%7Bname%3A%20%27rst_n%27%2C%20wave%3A%20%27101.....%7C...%7C..%27%7D%2C%0A%20%20%20%7Bname%3A%20%27we%27%2C%20wave%3A%20%270..1..0.%7C.10%7Cxx%27%2C%20node%3A%20%27...0%27%7D%2C%0A%20%20%20%7Bname%3A%20%27cmd%5B68%3A0%5D%27%2C%20wave%3A%20%270..335xx%7Cx4x%7Cxx%27%2C%20data%3A%20%5B%27key%5B63%3A0%5D%27%2C%20%27key%5B127%3A0%5D%27%2C%20%27round%27%2C%20%27finalize%27%5D%2C%20node%3A%20%27...1......%27%7D%2C%0A%20%20%5D%2C%0A%20%20%5B%27Result%27%2C%0A%20%20%09%7Bname%3A%20%27busy%27%2C%20wave%3A%20%270.....1.%7C.01%7C0.%27%2C%20node%3A%20%27......2%27%7D%2C%0A%20%20%20%7Bname%3A%20%27result%5B63%3A0%5D%27%2C%20wave%3A%20%270.......%7C...%7C2.%27%2C%20data%3A%20%5B%27result%27%5D%2C%20node%3A%20%27.............3%27%7D%0A%20%20%5D%0A%5D%2C%0A%20%20config%3A%20%7B%20hscale%3A%201.5%2C%20skin%3A%20%27default%27%20%7D%2C%0A%20%20head%3A%20%7B%0A%20%20text%3A%20%27SipHash%20module%20usage%27%0A%20%20%7D%0A%7D%0A" />

Use the module as follows:

1. Set the key before hashing anything. This can be done in one clock cycle.
2. Issue a round command and wait for a falling edge on `busy`. 
3. Issue further round commands. If you issue a new round command while the module is busy, you command will be ignored.
4. Issue a finalize command. Wait for `busy` going to low.
5. Read result from the result register.

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
