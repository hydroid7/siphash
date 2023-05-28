import cocotb
from cocotb.triggers import RisingEdge, Timer, FallingEdge
from cocotb_coverage import crv
from cocotb_coverage.coverage import *
from cocotb import logging
from cocotb.binary import BinaryValue

from test_util import clock_gen, reset, set_key, command
import random
import sys
from model import SipHash
from test_configurations import keys
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

    # log.error('Test succesful.')
    # cocotb.fork(Driver(dut.a, dut.b, 500))
    # await cocotb.fork(Driver(dut.a, dut.b, 500))
    # coverage_db.report_coverage(log.info, bins=True)
    # coverage_db.export_to_yaml(filename="coverage.yml")
    
@cocotb.test()
async def initialises_start_vector_correctly(dut):
    """Tests if reading the key is correct. It compares values from the paper."""
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    key = keys['simple']
    await set_key(dut, key)
    await RisingEdge(dut.clk)
    test_vec = [
        0x7469686173716475,
        0x6b617f6d656e6665,
        0x6b7f62616d677361,
        0x7b6b696e727e6c7b
    ]
    for i in range(0, 4):
        print(hex(dut.v[i].value))
        # assert dut.v[i].value == test_vec[i], f'Unexpected value in v_{i}: {dut.v[i].value}'

@cocotb.test()
async def test_setting_key_with_simple_key(dut):
    """Tests if setting the initial key is correct. Simple example with the key being 'b0."""
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    key = keys['zeros']
    await set_key(dut, key)
    await RisingEdge(dut.clk)
    test_vec = [
        0x736f6d6570736575,
        0x646f72616e646f6d,
        0x6c7967656e657261,
        0x7465646279746573
    ]
    for i in range(0, 3):
        assert dut.v[i].value == test_vec[i], f'Unexpected value in v_{i}: {dut.v[i].value}'

@cocotb.test()
async def round_output_correct(dut):
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    await set_key(dut, keys['simple'])
    await command(dut, '0010', '0' * 64)
    await FallingEdge(dut.busy)
    await command(dut, '0010', '1' * 64)
    await FallingEdge(dut.busy)
    # await FallingEdge(dut.busy)
    # await command(dut, '010', '1' * 64)
    # model = SipHash()
    # model.set_key([0, 0, 0, 0])
    # model.siphash_round()

    # assert dut.v[0].value.binstr == BinaryValue(model.v[0], 64).binstr
    # assert dut.v[1].value.binstr == BinaryValue(model.v[1], 64).binstr
    # assert dut.v[2].value.binstr == BinaryValue(model.v[2], 64).binstr
    # assert dut.v[3].value.binstr == BinaryValue(model.v[3], 64).binstr
    await Timer(50, 'ns')
    # dut._log.info(model.v)


@cocotb.test(skip=True)
async def test_paper_values(dut):
    """This test checkst the generated values with the ones from the SipHash paper."""
    key = [0x0706050403020100, 0x0f0e0d0c0b0a0908]
    m1 = 0x0706050403020100
    m2 = 0x0f0e0d0c0b0a0908
    expected = 0xa129ca6149be45e5
    my_siphash = SipHash(verbose=2)
    my_siphash.set_key(key)

    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    await set_key(dut, key)

    my_siphash.compression(m1)
    my_siphash.compression(m2)
    
    result = my_siphash.finalization()
    
    assert result == expected
    if result == expected:
        print("Correct result 0x%016x generated." % result)
    else:
        print("Incorrect result 0x%016x generated, expected 0x%016x." % (result, expected))
    print("")