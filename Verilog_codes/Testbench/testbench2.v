`timescale 1ns / 1ps

module tb_main;

    // Inputs
    reg clk;
    reg rst;
    reg [4:0] enable;

    // Output
    wire [639:0] encrypted128;

    // Instantiate the Unit Under Test (UUT)
    main uut (
        .clk(clk),
        .rst(rst),
        .enable(enable),
        .encrypted128(encrypted128)
    );

    // Clock generation
    initial clk = 0;
    always #5 clk = ~clk; // Generates a 100 MHz clock

    // Reset process
    initial begin
        rst = 1; // Assert reset
        enable = 0; // Disable all AES instances initially
        #40 rst = 0; // Deassert reset after 40ns
        #10 enable = 5'b11111; // Enable all AES instances after reset
    end

    // Simulation run
    initial begin
        #100; // Run the simulation for 100ns to observe behavior
        $finish; // End the simulation
    end

    // Print output at every positive edge of the clock after reset is deasserted
    always @(posedge clk) begin
        if (!rst) begin // Only print after reset is deasserted
            $display("Time = %t, Enable = %b, Encrypted Data = %h", $time, enable, encrypted128);
        end
    end

    // Monitoring Outputs
    initial begin
        $monitor("Time = %t, Encrypted Data = %h", $time, encrypted128);
    end

endmodule
