module counter #(
    parameter INITIAL_VAL=0
) (
    input clk,
    input rst_n,
    input trigger,
    output reg[3:0] out
);

localparam START_VAL = INITIAL_VAL-1;
reg is_running;

always @(posedge clk) begin
    if(~rst_n) begin
        out <= START_VAL;
        is_running <= 'b0;
    end else if(trigger) begin
        is_running <= 'b1;
    end else begin
        if (out == 'b0) begin
            out <= START_VAL;
            is_running <= 'b0;
        end else
            out <= out - {3'b0, is_running};
    end
end
endmodule