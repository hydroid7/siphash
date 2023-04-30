import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb_coverage import crv
from cocotb_coverage.coverage import *
from cocotb import logging
from cocotb.binary import BinaryValue

from test_util import clock_gen, reset, set_input
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

    # log.error('Test succesful.')
    # cocotb.fork(Driver(dut.a, dut.b, 500))
    # await cocotb.fork(Driver(dut.a, dut.b, 500))
    # coverage_db.report_coverage(log.info, bins=True)
    # coverage_db.export_to_yaml(filename="coverage.yml")
    

# @cocotb.test()
# async def busy_high_while_calculation(dut):
#     cocotb.start_soon(clock_gen(dut.clk))
#     await reset(dut.rst_n)
#     assert True == False


@cocotb.test()
async def initialises_start_vector_correctly(dut):
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    key = [
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
    await set_input(dut, key, None)
    await RisingEdge(dut.clk)
    assert dut.key[0].value == 0, 'Key is not set.'
    await Timer(20, 'ns')
    dut.start.value = 1
    await Timer(5, 'ns')
    dut.start.value = 0
    await Timer(5, 'ns')

    ivs = [
        0x736f6d6570736575,
        0x646f72616e646f6d,
        0x6c7967656e657261,
        0x7465646279746573
    ]
    for i in range(0, 3):
        assert dut.v[i].value == ivs[i], f'Unexpected: IV is {dut.v[i].value}'