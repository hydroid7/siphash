module sip_half_round #(
    parameter V1_SHIFT = 13, 
    parameter V3_SHIFT = 16
) (
    input wire clk,
    input wire rst_n,
    input wire [63:0] v0_in,
    input wire [63:0] v1_in,
    input wire [63:0] v2_in,
    input wire [63:0] v3_in,

    output reg [63:0] v0_out,
    output reg [63:0] v1_out,
    output reg [63:0] v2_out,
    output reg [63:0] v3_out
);

wire [63:0] v1_shifted = (v1_in <<< V1_SHIFT);
wire [63:0] sum_v1_v0 = (v1_in + v0_in);
wire [63:0] sum_v2_v3 = (v2_in + v3_in);
wire [63:0] v3_shifted = (v3_in <<< V3_SHIFT);

always @(posedge clk) begin
    if(!rst_n) begin
        v0_out <= 0;
        v1_out <= 0;
        v2_out <= 0;
        v3_out <= 0;
    end else begin
        v1_out <= v1_shifted ^ sum_v1_v0;
        v0_out <= (sum_v1_v0 <<< 32);
        v2_out <= sum_v2_v3;
        v3_out <= (v3_shifted ^ sum_v2_v3);
    end
end

endmodule