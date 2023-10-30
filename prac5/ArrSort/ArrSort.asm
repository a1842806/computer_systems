// Sorts the array of length R2 whose first element is at RAM[R1] in ascending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R1
D=M
@R2
D=D+M
@last
M=D-1

(OUTER_LOOP)
@R2
M=M-1
D=M
@END
D;JEQ
@R1
D=M
@temp
M=D-1

(INNER_LOOP)
@temp
M=M+1
D=M
@last
D=D-M
@OUTER_LOOP
D;JEQ

@temp
A=M+1
D=M
@y
M=D
@temp
A=M
D=M
@x
M=D
@NEG
D;JLT

(POS)
@y
D=M
@SWAP
D;JLT
@CHECK
0;JMP

(NEG)
@y
D=M
@INNER_LOOP
D;JGE
@CHECK
0;JMP

(CHECK)
@x
D=M
@y
D=D-M
@SWAP
D;JGT
@INNER_LOOP
0;JMP

(SWAP)
@temp
A=M
D=M
@x
M=D
@temp
A=M+1
D=M
@temp
A=M
M=D
@x
D=M
@temp
A=M+1
M=D
@INNER_LOOP
0;JMP

(END)
@R0
M=-1
@END
0;JMP
