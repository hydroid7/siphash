import cocotb
from cocotb.triggers import RisingEdge
import random
import sys
from model import SipHash

@cocotb.test()
async def basic_round(dut):
    """Test for executing a basic round"""
    print(sys.path)
    SipHash()
    assert False == True