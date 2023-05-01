`default_nettype none

module siphash(
    input wire clk,
    input wire rst_n,
    input wire start,

    input wire [255:0] key,
    /* verilator lint_off UNUSED */
    input wire [63:0] nonce,

    output reg done,
    output reg [63:0] result,
    /* verilator lint_off UNDRIVEN */
    output reg busy
);

reg [63:0] v [3:0];
reg [63:0] iv [3:0];

assign iv[0] = 64'h736f6d6570736575;
assign iv[1] = 64'h646f72616e646f6d;
assign iv[2] = 64'h6c7967656e657261;
assign iv[3] = 64'h7465646279746573;

generate
    genvar i;
    for (i = 0; i <= 3; i = i + 1) begin
        always @(posedge clk) begin
            if(start && rst_n) begin
                v[i] <= key[64*i+63:64*i] ^ iv[i];
            end
        end
    end
endgenerate

sip_round first_round (
    .clk(clk),
    .rst_n(rst_n),
    .iv0(iv[0]),
    .iv1(iv[1]),
    .iv2(iv[2]),
    .iv3(iv[3])
);

always @(posedge clk) begin
    if(~rst_n) begin
        done <= 0;
        result <= 0;
    end
end

`ifdef COCOTB_SIM
    initial begin
        $dumpfile("siphash.vcd");
        $dumpvars(0, siphash);
        $dumpvars(0, v[0]);
        $dumpvars(0, v[1]);
        $dumpvars(0, v[2]);
        $dumpvars(0, v[3]);
        #1;
    end
`endif

endmodule