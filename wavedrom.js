{
    signal: [
        { name: 'clk', wave: 'p.......|...|..' },
        ['Control',
            { name: 'rst_n', wave: '101.....|...|..' },
            { name: 'we', wave: '0..1..0.|.10|xx', node: '...0' },
            { name: 'cmd[68:0]', wave: '0..335xx|x4x|xx', data: ['key[63:0]', 'key[127:0]', 'round', 'finalize'], node: '...1......' },
        ],
        ['Result',
            { name: 'busy', wave: '0.....1.|.01|0.', node: '......2' },
            { name: 'result[63:0]', wave: '0.......|...|2.', data: ['result'], node: '.............3' }
        ]
    ],
    config: { hscale: 1.5, skin: 'default' },
    head: {
        text: 'SipHash module usage'
    }
}
