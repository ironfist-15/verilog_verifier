This project aims to solve the problem of reliably verifying the correctness of a digital hardware module without manual inspection or waveform analysis. As designs grow even moderately complex, manually checking outputs or relying only on HDL testbenches becomes error-prone and hard to scale.
The goal is to create a simple, repeatable, and automated verification flow that works entirely from the Linux command line and can be extended to larger designs or continuous integration environments .
To separate the responsibilities , Python creates different inputs for the testbench code , this is wriiten to the file tests.txt , then the testbench parses this file and calculates the results , the test case along with the results are stored in sim.log file .
Then the next command calls Python to verify the results stored in sim.log , then python shows the number of test cases ran on th eterminal .
This approach keeps the hardware design, checking logic, and automation independent, making the system easier to debug, maintain, and extend.



!#/usr/bin/bash

set -e
set -x
echo -e "creating test cases in python"
python3 scripts/verify_results.py --generate


echo -e "compiling and execute the verilog and testbench\n"
iverilog rtl/alu.v tb/tb_alu.v -o alu_sim

vvp alu_sim | tee logs/sim.log

echo -e "verifying the iutput of testbench in python\n"
python3 scripts/verify_results.py --check logs/sim.log
~


