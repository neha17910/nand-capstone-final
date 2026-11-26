# Make the Computer Draw a Box
Neha | 2501730466 | B.Tech CSE (AI & ML), Semester 3

K = 66; width = 48 pixels; height = 20; start = 16384 + 32*66 = 18496.

## Part A
Copy the three HDL files into the Nand2Tetris projects/05 folder (back up existing files). Use the Hardware Simulator to load and run CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst and ComputerRect.tst. Capture each result. Standard simulator chips are used for dependencies (including ARegister, DRegister, RAM16K, Screen, Keyboard and ROM32K); local lab chips can be supplied where compatible.

## Part B
Run `python assembler.py Box.asm` in this folder. This creates Box.hack and symbols.txt. To test Add, Max, Rect and Pong, copy their official ASM files into separate test folders, assemble each using `python assembler.py path/to/Add.asm` (substitute filename), and compare its output with the official Assembler output saved separately. Keep the Box symbols.txt unchanged by using separate folders.

## Part C
Open CPU Emulator, load Box.hack, select No animation and run. Enable keyboard input and hold a key: a black box should appear at row 66, columns 0–47. Release the key: it should disappear. Capture actual output.

## Viva
A-instruction sets A; C-instruction computes, stores and jumps. CPU uses ALU, registers and PC. Memory selects RAM, screen or keyboard. Pass 1 finds labels; pass 2 converts instructions and allocates variables from RAM16. Each screen row is 32 words. To move the box down one row, change 18496 to 18528 and assemble again.

Official simulator tests and screenshots are pending; do not claim they passed until you run them.
