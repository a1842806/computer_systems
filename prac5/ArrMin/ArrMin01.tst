// Sample Test file for ArrMin.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrMin.asm,
output-file ArrMin01.out,
compare-to ArrMin01.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[20]%D2.6.2 RAM[21]%D2.6.2 RAM[22]%D2.6.2 RAM[23]%D2.6.2;

set PC 0,
set RAM[0]  0,  // Set R0
set RAM[1]  5, // Set R1
set RAM[2]  3,  // Set R2
set RAM[5] 100, 
set RAM[6] 90,  
set RAM[7] 80,  
set RAM[23] 3;  
repeat 300 {
  ticktock;    // Run for 300 clock cycles
}
set RAM[1]  5, // Set R1
set RAM[2]  3,  // Set R2
set RAM[5] 100, 
set RAM[6] 90,  
set RAM[7] 80,  
set RAM[23] 3,
output;        // Output to file

