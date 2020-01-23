// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


@8192   // (512 * 32) / 16
D=A
@n
M=D     // count = 8192 (# of bytes)

(RESET)
        @i
        M=0     // index = 0

(KEYBOARD)
        @KBD
        D=M
        @WHITE
        D;JEQ   // goto WHITE if KBD value is 0

(BLACK)
        @i
        D=M
        @SCREEN
        A=A+D   // Calculate byte address
        M=-1    // Fill with black
        @DECISION
        0;JMP   // goto END
(WHITE)
        @i
        D=M
        @SCREEN
        A=A+D   // Calculate byte address
        M=0     // Fill with white

(DECISION)   
        @i
        MD=M+1  // Increment index by 1
        @n
        D=D-M
        @RESET
        D;JEQ   // goto LOOP if count - index == 0
        @KEYBOARD
        0;JMP   // goto INNER