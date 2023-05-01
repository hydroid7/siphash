from cocotb.triggers import RisingEdge

class TestConfiguration:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = nonce

    async def set_values(self, dut):
        await RisingEdge(dut.clk)
        dut.key = self.key
        dut.nonce = self.nonce

# TODO generate test configurations here:
# cases = [
#     TestConfiguration()
# ]

keys = {
    'simple': [
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    ]
}
    