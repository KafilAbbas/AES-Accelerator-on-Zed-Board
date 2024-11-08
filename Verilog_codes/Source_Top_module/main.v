module main (
    input clk
);
    wire rst;
    reg [4:0] enable = 5'b00001; // Set enable[0] to 1
    reg [128*5-1:0] encrypted128;
    wire [639:0] ila_data;
    reg [7:0] bram_address;
    wire [127:0] key128 = 128'h000102030405060708090a0b0c0d0e0f; // Static AES key
    wire [127:0] in_array [4:0];
    wire [127:0] encrypted128_array [4:0];
    wire [639:0] bram_data_out;
    wire [639:0] dina;

    // Instantiate Block RAM
    blk_mem_gen_0 BRAM (
      .clka(clk),            // input wire clka
      .ena(1'b1),            // input wire ena
      .wea(1'b0),            // input wire [0 : 0] wea
      .addra(bram_address),  // input wire [5 : 0] addra
      .dina(dina),           // input wire [639 : 0] dina
      .douta(bram_data_out)  // output wire [639 : 0] douta
    );

    // Assign each portion of the BRAM output to in_array
    assign in_array[0] = bram_data_out[127:0];
    assign in_array[1] = bram_data_out[255:128];
    assign in_array[2] = bram_data_out[383:256];
    assign in_array[3] = bram_data_out[511:384];
    assign in_array[4] = bram_data_out[639:512];

    // Instantiate AES encryption modules
    generate
        genvar i;
        for (i = 0; i < 5; i = i + 1) begin : aes_instances
            AES_Encrypt aes_encrypt ( 
                .in(in_array[i]),
                .key(key128),
                .out(encrypted128_array[i])
            );
        end
    endgenerate

    // Flatten the encrypted outputs for ILA
    always @(posedge clk) begin
        encrypted128[127:0]   <= encrypted128_array[0];
        encrypted128[255:128] <= encrypted128_array[1];
        encrypted128[383:256] <= encrypted128_array[2];
        encrypted128[511:384] <= encrypted128_array[3];
        encrypted128[639:512] <= encrypted128_array[4];
    end

    // Output to ILA
    assign ila_data = {encrypted128};

    // ILA instantiation
    ila_0 ila_core (
        .clk(clk),
        .probe0(ila_data),
        .probe1(bram_address)
    );

    vio_1 my_VIO (
      .clk(clk),       // input wire clk
      .probe_out0(rst) // output wire [0 : 0] probe_out0
      // .probe_out1(enable) // Uncomment if you want to control 'enable' via VIO
    );

    // Declare a delay counter
    reg [7:0] delay_counter;

    // Always block for BRAM address updating with delay
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            bram_address  <= 0;
            delay_counter <= 0;
        end else if (enable[0] && bram_address < 55) begin
            if (delay_counter == 4) begin  // Adjust this value for desired delay
                bram_address  <= bram_address + 1; // Increment address after delay
                delay_counter <= 0;                // Reset delay counter
            end else begin
                delay_counter <= delay_counter + 1; // Increment delay counter
            end
        end
    end

endmodule
