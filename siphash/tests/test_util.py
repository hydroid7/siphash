from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue

# @cocotb.coroutine
async def clock_gen(signal, period=2):
    while True:
        signal.value = 0
        await Timer(period / 2, units='ns')
        signal.value = 1
        await Timer(period / 2, units='ns')

# @cocotb.coroutine
async def reset(rst_n):
    await Timer(10, 'ns')
    rst_n.value = 1
    await Timer(10, 'ns')
    rst_n.value = 0
    await Timer(10, 'ns')
    rst_n.value = 1
    
async def set_input(dut, key, nonce):
    await RisingEdge(dut.clk)
    dut.key.value = BinaryValue(''.join(["{0:b}".format(x) for x in key]))
    dut.nonce.value = BinaryValue(nonce)