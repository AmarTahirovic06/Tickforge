module shift_reg (
    input logic     clk,
    input logic    rst_n,
    input logic    [7:0] data_in,
    input logic     valid, 
    output logic    [15:0] data_out
);

    always_ff @(posedge clk) begin 
        if (!rst_n) begin
            data_out <= 16'd0; 
        end else if (valid) begin
            data_out <= {data_out[7:0], data_in};
        end
    end
endmodule