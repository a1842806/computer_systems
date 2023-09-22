// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R1
A=M
D=M
@R0
M=D

(LOOP)
@R2
M=M-1
D=M
@END
D;JEQ
@R1
AM=M+1
D=M
@R0
D=D-M

@LOOP
D;JGT
@R1
A=M
D=M
@R0
M=D
@LOOP
0;JMP

(END)
@END
0;JMP
