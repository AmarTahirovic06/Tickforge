module shift_reg #(parameter WIDTH = 16) (
    input logic     clk,
    input logic    rst_n,
    input logic [7:0] data_in,
    input logic     valid, 
    output logic   [WIDTH-1:0] data_out
);

    always_ff @(posedge clk) begin 
        if (!rst_n) begin
            data_out <= '0; 
        end else if (valid) begin
            data_out <= {data_out[WIDTH-9:0], data_in};
        end
    end
endmodule