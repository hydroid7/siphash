`default_nettype none
module siphash #(
    parameter C = 2,
    parameter D = 4
) (
    input wire clk,
    input wire rst_n,
    input wire we,
    input wire [64+4-1:0] cmd,

    output reg busy,
    output reg [63:0] result
);

`define ROUND_START 'b0001
`define ROUND_END   'b0010
`define ROUND_ROUND 'b0011

counter #(.INITIAL_VAL(D)) round_counter (
    .clk(clk),
    .rst_n(rst_n),
    .trigger(counter_trigger),
    .out(counter_round)
);

sip_round round (
    // .clk(clk),
    // .rst_n(rst_n),
    .iv0(iv[0]),
    .iv1(iv[1]),
    .iv2(iv[2]),
    .iv3(iv[3]),
    
    .ov0(ov[0]),
    .ov1(ov[1]),
    .ov2(ov[2]),
    .ov3(ov[3])
);

// counter #(.INITIAL_VAL(D)) final_counter (
//     .clk(clk),
//     .rst_n(rst_n),
//     .out(final_round)
// );

reg [3:0] counter_round;
reg counter_trigger;

wire [3:0] opcode = cmd[67:64];
wire [63:0] data = cmd[63:0];

/* verilator lint_off UNUSED */
reg [63:0] next_data;
reg [3:0] state;

reg [63:0] v [3:0];
reg [63:0] initial_vector [3:0];

reg [63:0] iv [3:0];
reg [63:0] ov [3:0];

assign initial_vector[0] = 64'h736f6d6570736575;
assign initial_vector[1] = 64'h646f72616e646f6d;
assign initial_vector[2] = 64'h6c7967656e657261;
assign initial_vector[3] = 64'h7465646279746573;

always @(posedge clk) begin
    if(~rst_n) begin
        result <= 0;
        busy <= 0;
        counter_trigger <= 0;
        state <= 0;
        for (integer i = 0; i < 4; i++) begin
            iv[i] <= 0;
        end
    end else if(we && !busy) begin
        // Read key first part
        if (opcode == 'b0000) begin
            v[0] <= data ^ initial_vector[0];
            v[2] <= data ^ initial_vector[2];
            busy <= 'b0;
        // Read key second part
        end else if (opcode == 'b0001) begin
            v[1] <= data ^ initial_vector[1];
            v[3] <= data ^ initial_vector[3];
            busy <= 'b0;
        // Compression
        end else if (opcode == 'b0010) begin
            v[3] <= v[3] ^ data;
            next_data <= data;
            busy <= 'b1;
            counter_trigger <= 'b1;
            state <= `ROUND_START;
        // Finalize
        end else if (opcode == 'b0011) begin
            v[2] <= v[2] ^ 'hff;
        end else
            $display("Invalid opcode %b", opcode);
    end else begin
        if (state == `ROUND_START) begin
            counter_trigger <= 'b0;
            state <= `ROUND_ROUND;
            iv[0] <= v[0];
            iv[1] <= v[1];
            iv[2] <= v[2];
            iv[3] <= v[3];
        end else if (state == `ROUND_ROUND) begin
            if(counter_round == 1)
                state <= `ROUND_END;
            $display("State round %d", counter_round);
            iv[0] <= ov[0];
            iv[1] <= ov[1];
            iv[2] <= ov[2];
            iv[3] <= ov[3];
            // TODO do here the round
        end else if (state == `ROUND_END) begin
            v[0] <= ov[0];
            v[1] <= ov[1];
            v[2] <= ov[2];
            v[3] <= ov[3];
            busy <= 'b0;
            state <= 0;
            // TODO update state 
        end
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