`timescale 1ns/1ps

module tb_alu;

    reg  [7:0] a;
    reg  [7:0] b;
    reg  [1:0] op;
    wire [7:0] result;

    integer file;
    integer status;
    reg [31:0] op_str;   // simpler string storage

    alu dut (
        .a(a),
        .b(b),
        .op(op),
        .result(result)
    );

    initial begin
        file = $fopen("tests.txt", "r");
        if (file == 0) begin
            $display("ERROR: could not open tests.txt");
            $finish;
        end

        while (1) begin
            status = $fscanf(file, "%d %d %s", a, b, op_str);
            if (status != 3)
                $finish;

            if (op_str == "ADD")      op = 2'b00;
            else if (op_str == "SUB") op = 2'b01;
            else if (op_str == "AND") op = 2'b10;
            else if (op_str == "OR")  op = 2'b11;
            else                      op = 2'b00;

            #5;
            $display("A=%0d B=%0d OP=%s RESULT=%0d",
                     a, b, op_str, result);
            #5;
        end
    end

endmodule
