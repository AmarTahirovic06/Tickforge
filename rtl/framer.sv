typedef enum logic {S_LEN, S_BODY} state_t;
module framer
( 
    input logic clk, 
    input logic rst_n, 
    input logic [7:0] data_in, 
    input logic valid,
    output state_t state
); 
    logic [7:0] len_high;
    logic [15:0] byte_count; 
    logic len_phase; 

always_ff @(posedge clk) begin
    if (!rst_n) begin
        state <= S_LEN; 
        len_phase <= 1'b0; 
    end else if (valid) begin 
        if (state == S_LEN) begin
            if (len_phase == 0) begin 
        len_high <= data_in;
        len_phase <= 1; 
        end else begin 
        byte_count <= {len_high, data_in}; 
        len_phase <= 0; 
        state <= S_BODY;
        end 
        end else begin 
            if  (byte_count == 16'd1) begin
            state <= S_LEN;
        end else begin
        byte_count <= byte_count -1;
            end
        end
    end
end
        endmodule

