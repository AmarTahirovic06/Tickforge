module counter (
    input logic clk,
    input logic rst_n,
    output logic [4:0]count
);

    always_ff @(posedge clk) begin
        if (!rst_n)
            count <= 4'd0;
    else  
        end