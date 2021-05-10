# Post machine Emulator

The Post machine is a universal performer (abstract computing machine), based on the ideas of the work of the American mathematician E. L. Post, whose goal was to clarify the concept of an algorithm. According to the Post's thesis, any algorithm can be written as a program for the Post machine.

The Post machine consists of a carriage (reading and writing head) and an infinite tape divided into cells. Each cell in the feed can be either empty or contain a label. 

The program consists of numbered lines. Each line contains one of the following commands:

- \>N move the carriage to the right by 1 cell and go to the row with the number N
- \<N move the carriage to the left by 1 cell and go to the row with the number N
- x N erase the label and go to the line with the number N
- \+ N put a label and go to the line with the number N
- ? N, M if the current cell is not marked, then go to the row with the number N, otherwise go to the row M
- !   stop the program

## Installing the program
The program can be installed on `Linux` / `macOS` / `Windows`.
To install, select one of the packages:
 - Linux link
 - Mac link
 - Windows link


## How to work with the program?

In the upper part of the program there is an editor field where you can enter the task condition in a free form.

The ribbon moves left and right using the buttons located to the left and right of it. 

In the table at the bottom of the window, the program is typed. The first column contains the line numbers and is filled in automatically. In the second column, enter the desired command, and in the third column, enter the line number to go to.

The fourth column can contain a comment on each line of the program. You can add, delete, or clear table rows using the buttons located at the top of the table.

The program can be executed continuously or in steps. The command that will be executed now is highlighted. The execution speed is adjusted using the `Pause` menu located in the upper-right corner.

In the right part there is a menu of tests (feeds), using the buttons located on the top you can add or remove tests. You can click to select one of the sets.

Tasks for the Post machine can be saved in files. The task condition, the program, the status of the feed, and the type of marks are saved. The tests are saved separately. They can be connected to any program.
