`default_nettype none

module sip_round (
    input clk, 
    input rst_n, 
    input [63:0] iv0, iv1, iv2, iv3, 
    output [63:0] ov0, ov1, ov2, ov3
);

reg  [63:0] v0, v1, v2, v3;
reg  [63:0] i0, i1, i2, i3;

sip_half_round first_half (
    .clk(clk),
    .rst_n(rst_n),

    .v0_in(iv0),
    .v1_in(iv1),
    .v2_in(iv2),
    .v3_in(iv3),

    .v0_out(v2),
    .v1_out(v1),
    .v2_out(v0),
    .v3_out(v3)
);

sip_half_round #(
    .V1_SHIFT(17),
    .V3_SHIFT(21)
) second_half (
    .clk(clk),
    .rst_n(rst_n),

    .v0_in(v0),
    .v1_in(v1),
    .v2_in(v2),
    .v3_in(v3),

    .v0_out(ov2),
    .v1_out(ov1),
    .v2_out(ov0),
    .v3_out(ov3)
);

endmodule


