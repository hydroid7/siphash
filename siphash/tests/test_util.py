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
    
async def set_key(dut, key):
    await RisingEdge(dut.clk)
    dut.cmd.value = BinaryValue(value='0000' + '{:b}'.format(key[0]), n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.we.value = 0
    await RisingEdge(dut.clk)
    print(f'{key[0]:b}')
    print(f'{key[0]:x}')
    dut.cmd.value = BinaryValue('0001' + '{:b}'.format(key[1]), n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.we.value = 0

async def command(dut, cmd, data):
    dut.cmd.value = BinaryValue(cmd + data, n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.we.value = 0