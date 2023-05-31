from cocotb.triggers import Timer, RisingEdge
from cocotb.binary import BinaryValue

async def _command(dut, cmd, data):
    formatted = '{:064b}'.format(data)
    dut.cmd.value = BinaryValue(cmd + formatted, n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.we.value = 0

async def clock_gen(signal, period=2):
    while True:
        signal.value = 0
        await Timer(period / 2, units='ns')
        signal.value = 1
        await Timer(period / 2, units='ns')

async def reset(rst_n):
    await Timer(10, 'ns')
    rst_n.value = 1
    await Timer(10, 'ns')
    rst_n.value = 0
    await Timer(10, 'ns')
    rst_n.value = 1
    
async def set_key(dut, key):
    await RisingEdge(dut.clk)
    dut.cmd.value = BinaryValue('0000' + '{:064b}'.format(key[0]), n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.cmd.value = BinaryValue('0001' + '{:064b}'.format(key[1]), n_bits=68)
    dut.we.value = 1
    await RisingEdge(dut.clk)
    dut.we.value = 0

async def compress(dut, data):
    await _command(dut, '0010', data)

async def finalize(dut):
    await _command(dut, '0011', 0x0)

def assert_state(dut, internal_state):
    if len(internal_state) != 4:
        raise ValueError(f"Length of internal_state should be 4, got {len(internal_state)} instead.")
    for i in range(0, 4):
        assert dut.v[i].value == internal_state[i], f'Unexpected value in v_{i} ≠ expected.'

def assert_result(dut, expected):
    assert dut.result.value == '{:064b}'.format(expected)