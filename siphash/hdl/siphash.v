`default_nettype none

module siphash(
    input wire clk,
    input wire rst_n,
    input wire we,
    input wire cs,

    input wire [0:255] key,
    input wire [0:63] nonce,

    output reg done,
    output reg [0:63] result,
    output reg busy
);

always @(posedge clk) begin
    if(~rst_n) begin
        done <= 0;
        result <= 0;
    end
end

`ifdef COCOTB_SIM
    initial begin
        $dumpfile ("siphash.vcd");
        $dumpvars (0, siphash);
        #1;
    end
`endif

endmodule