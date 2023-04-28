import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb_coverage import crv
from cocotb_coverage.coverage import *
from cocotb import logging

from test_util import clock_gen, reset
import random
import sys
from model import SipHash

# class rand_input(crv.Randomized):
#     def __init__(self):
#         crv.Randomized.__init__(self)
#         self.a = 0
#         self.b = 0
#         self.add_rand("a", [0, 0, 1, 1])
#         self.add_rand("b", [0, 1, 1, 0])

# @cocotb.coroutine
# def Driver(signal1, signal2, N):
#     ri = rand_input()
#     for _ in range(N):
#         ri.randomize()
#         signal1.value = ri.a
#         signal2.value = ri.b
#         yield Timer(1, 'ns')

# @cocotb.coroutine
# def Checker(dut, N):
#     for _ in range(N):
#         yield Timer(1, 'ns')
#         assert dut.c == (dut.a.value + dut.b.value)

@cocotb.test()
async def dut_reset_ok(dut):
    log = cocotb.logging.getLogger('reset.test')
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    assert int(dut.result.value) == 0
    assert dut.done.value == 0

    log.error('Test succesful.')
    # cocotb.fork(Driver(dut.a, dut.b, 500))
    # await cocotb.fork(Driver(dut.a, dut.b, 500))
    # coverage_db.report_coverage(log.info, bins=True)
    # coverage_db.export_to_yaml(filename="coverage.yml")
    

@cocotb.test()
async def busy_high_while_calculation(dut):
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    assert True == False

