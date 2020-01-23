// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// pseudo code
// i=0;
// n=RAM[0]
// for (i=0; i<n; i++){
//      RAM[2] += RAM[1]
// }

// i=0
@i
M=0

@R2
M=0

(LOOP)

// if i == n, goto END
@i
D=M
@R0
D=D-M
@END
D;JGE

// i++
@i
M=M+1

// RAM[2] += RAM[1]
@R1
D=M
@R2
M=D+M

@LOOP
0;JMP

(END)
@END
0;JMP