
module round (
    input clk, 
    input rst_n, 
    input [63:0] iv0, iv1, iv2, iv3, 
    output [63:0] ov0, ov1, ov2, ov3
);

    reg  [63:0] add_0_res, add_1_res, add_2_res, add_3_res;
    reg  [63:0] v0_tmp, v1_tmp, v2_tmp, v3_tmp;
    reg  [63:0] v0, v1, v2, v3;
    reg  [63:0] i0, i1, i2, i3;

    always @(posedge clk)
    begin
        if (~rst_n)
        begin
            i0 <= 0;
            i1 <= 0;
            i2 <= 0;
            i3 <= 0;
        end else
        begin
            i0 <= iv0;
            i1 <= iv1;
            i2 <= iv2;
            i3 <= iv3;
        end
    end

    always @*
    begin
        add_0_res = i0 + i1;
        add_1_res = i2 + i3;

        v0_tmp = {add_0_res[31:0], add_0_res[63:32]};
        v1_tmp = {i1[50:0], i1[63:51]} ^ add_0_res;
        v2_tmp = add_1_res;
        v3_tmp = {i3[47:0], i3[63:48]} ^ add_1_res;    

        add_2_res = v1_tmp + v2_tmp;
        add_3_res = v0_tmp + v3_tmp;

        v0 = add_3_res;
        v1 = {v1_tmp[46:0], v1_tmp[63:47]} ^ add_2_res;
        v2 = {add_2_res[31:0], add_2_res[63:32]};
        v3 = {v3_tmp[42:0], v3_tmp[63:43]} ^ add_3_res;         
    end

    assign ov0 = v0;
    assign ov1 = v1;
    assign ov2 = v2;
    assign ov3 = v3;  
endmodule