module swap (
    input wire [63:0] in_a,
    input wire [63:0] in_b,
    output wire [63:0] out_a,
    output wire [63:0] out_b
);
    assign out_b = in_a;
    assign out_a = in_b;
endmodule