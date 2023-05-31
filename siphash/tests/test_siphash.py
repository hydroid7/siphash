import cocotb
from cocotb.triggers import RisingEdge, Timer, FallingEdge
from cocotb_coverage import crv
from cocotb_coverage.coverage import *

from test_util import clock_gen, reset, set_key, compress, finalize, assert_state, assert_result
from model import SipHash
from test_configurations import keys

@cocotb.test()
async def dut_reset_ok(dut):
    log = cocotb.logging.getLogger('reset.test')
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    assert int(dut.result.value) == 0
    
@cocotb.test()
async def sets_the_key_correctly(dut):
    """Tests if setting the of the encryption key is correct. It compares values from the paper."""
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    key = keys['paper']
    await set_key(dut, key)
    await RisingEdge(dut.clk)
    test_vec = [
        0x7469686173716475,
        0x6b617f6d656e6665,
        0x6b7f62616d677361,
        0x7b6b696e727e6c7b
    ]
    assert_state(dut, test_vec)

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
    assert_state(dut, test_vec)

@cocotb.test()
async def test_paper_values(dut):
    """This test checkst the generated values with the ones from the SipHash paper."""
    key = [0x0706050403020100, 0x0f0e0d0c0b0a0908]
    m1 = 0x0706050403020100
    m2 = 0x0f0e0d0c0b0a0908
    expected = 0xa129ca6149be45e5
    my_siphash = SipHash()
    my_siphash.set_key(key)

    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    await set_key(dut, key)
    my_siphash.compression(m1)
    my_siphash.compression(m2)
    await compress(dut, m1)
    await compress(dut, m2)
    result = my_siphash.finalization()
    await finalize(dut)
    assert_result(dut, expected)
    assert result == expected
    if result == expected:
        print("Correct result 0x%016x generated." % result)
    else:
        print("Incorrect result 0x%016x generated, expected 0x%016x." % (result, expected))


@cocotb.test()
async def round_output_correct(dut):
    '''Tests if the round outputs are the same, as the test values from the paper.'''
    from random import getrandbits
    h = SipHash()
    cocotb.start_soon(clock_gen(dut.clk))
    await reset(dut.rst_n)
    await RisingEdge(dut.clk)
    await set_key(dut, keys['paper'])
    h.set_key(keys['paper'])
    await RisingEdge(dut.clk)
    assert_state(dut, h.state())
    for i in range(1000):
        m = getrandbits(64)
        await compress(dut, m)
        h.compression(m)
        await FallingEdge(dut.busy)
        assert_state(dut, h.state())
