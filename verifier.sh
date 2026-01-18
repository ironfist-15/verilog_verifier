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
