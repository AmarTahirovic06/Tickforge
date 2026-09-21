module symbol_lookup (
    input logic clk, 
    input logic [63:0] data_in, 
    input logic in_valid, 
    output logic [9:0] symbol_index,
    output logic out_valid 
);
    logic [31:0] crc_value;
    logic [9:0] symbol_table [0:131071];

    crc32 crc_inst (
        .data_in (data_in),
        .crc_out (crc_value)
    );
    initial begin 
        $readmemh("../../tools/symbol_table.mem", symbol_table);
    end

    always_ff @(posedge clk) begin
        symbol_index <= symbol_table[crc_value[16:0]];
        out_valid <= in_valid;
    end
endmodule

        



