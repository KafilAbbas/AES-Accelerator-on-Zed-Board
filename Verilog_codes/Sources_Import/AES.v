module AES(clk, enable, in, encrypted128);
  input clk;
  input [4:0] enable;              // Enable signals for each AES instance
  input [128*5-1:0] in;            // Flattened input data for all instances
  output [128*5-1:0] encrypted128; // Flattened encrypted output for all instances

  wire [127:0] key128 = 128'h000102030405060708090a0b0c0d0e0f; // Static AES key

  // Separate each instance's input and output
  wire [127:0] in_array [4:0];
  wire [127:0] encrypted128_array [4:0];

  // Assign each portion of the flat input to in_array
  assign in_array[0] = in[127:0];
  assign in_array[1] = in[255:128];
  assign in_array[2] = in[383:256];
  assign in_array[3] = in[511:384];
  assign in_array[4] = in[639:512];

  // AES encryption instances
  AES_Encrypt a (
    .in(in_array[0]),
    .key(key128),
    .out(encrypted128_array[0])
  );

  AES_Encrypt b (
    .in(in_array[1]),
    .key(key128),
    .out(encrypted128_array[1])
  );

  AES_Encrypt c (
    .in(in_array[2]),
    .key(key128),
    .out(encrypted128_array[2])
  );

  AES_Encrypt d (
    .in(in_array[3]),
    .key(key128),
    .out(encrypted128_array[3])
  );

  AES_Encrypt e (
    .in(in_array[4]),
    .key(key128),
    .out(encrypted128_array[4])
  );

  // Assign each encrypted output to the correct portion of the flat output
  assign encrypted128[127:0]     = encrypted128_array[0];
  assign encrypted128[255:128]   = encrypted128_array[1];
  assign encrypted128[383:256]   = encrypted128_array[2];
  assign encrypted128[511:384]   = encrypted128_array[3];
  assign encrypted128[639:512]   = encrypted128_array[4];

endmodule
