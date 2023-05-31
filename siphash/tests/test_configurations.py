from cocotb.triggers import RisingEdge

keys = {
    'paper': [
        0x0706050403020100, 0x0f0e0d0c0b0a0908
    ],
    'zeros': [
        0x0000000000000000, 0x0000000000000000
    ]
}

plaintexts = {
    'first': ["{:>08b}".format(x) for x in range(0, 64)]
}

