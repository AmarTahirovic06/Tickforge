module crc32 (
    input logic [63:0] data_in,
    output logic [31:0] crc_out
);

    logic [31:0] crc;

    always_comb begin
        crc = 32'hFFFFFFFF;
        for (int b = 0; b < 8; b++) begin 
            for (int k = 0; k < 8; k++) begin
            crc[0] = crc[0] ^ data_in[56 - b*8 + k];
        if (crc[0])
            crc = (crc >> 1) ^ 32'hEDB88320;
        else 
            crc = crc >> 1; 
        end
    end
        crc_out = crc ^ 32'hFFFFFFFF;
end
endmodule
        



