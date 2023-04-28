import cocotb
from cocotb.triggers import Timer

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
    rst_n.value = 0
    await Timer(10, 'ns')
    rst_n.value = 1 