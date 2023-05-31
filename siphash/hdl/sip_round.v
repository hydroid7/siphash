`default_nettype none

module sip_round (
    input [63:0] iv0, iv1, iv2, iv3, 
    output [63:0] ov0, ov1, ov2, ov3
);

    wire [63:0] v0, v1, v2, v3;


    wire [63:0] add_0_res = iv0 + iv1;
    wire [63:0] add_1_res = iv2 + iv3;

    wire [63:0] v0_tmp = {add_0_res[31:0], add_0_res[63:32]};
    wire [63:0] v1_tmp = {iv1[50:0], iv1[63:51]} ^ add_0_res;
    wire [63:0] v2_tmp = add_1_res;
    wire [63:0] v3_tmp = {iv3[47:0], iv3[63:48]} ^ add_1_res;    

    wire [63:0] add_2_res = v1_tmp + v2_tmp;
    wire [63:0] add_3_res = v0_tmp + v3_tmp;

    assign ov0 = add_3_res;
    assign ov1 = {v1_tmp[46:0], v1_tmp[63:47]} ^ add_2_res;
    assign ov2 = {add_2_res[31:0], add_2_res[63:32]};
    assign ov3 = {v3_tmp[42:0], v3_tmp[63:43]} ^ add_3_res;  

    // sip_half_round #(
    //     .V1_SHIFT(13), 
    //     .V3_SHIFT(16)
    // ) first_half (
    //     .v0_in(iv0),
    //     .v1_in(iv1),
    //     .v2_in(iv2),
    //     .v3_in(iv3),

    //     .v0_out(v0),
    //     .v1_out(v1),
    //     .v2_out(v2),
    //     .v3_out(v3)
    // );

    // sip_half_round  #(
    //     .V1_SHIFT(17), 
    //     .V3_SHIFT(21)
    // ) second_half (
    //     .v0_in(v2),
    //     .v1_in(v1),
    //     .v2_in(v0),
    //     .v3_in(v3),

    //     .v0_out(ov2),
    //     .v1_out(ov1),
    //     .v2_out(ov0),
    //     .v3_out(ov3)
    // );

endmodule


