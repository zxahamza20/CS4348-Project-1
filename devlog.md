# 10-13-2026 11:50am

This is my first entry for the project. I have the basic understanding of the how the project works. The system is basically three separate programs, a logger, an encryption program, and a driver. I only run the driver. It launches the other two as child processes and talks to them through pipes. The logger writes lines like YYYY-MM-DD HH:MM ACTION MESSAGE to a file on the command line, and then stops when it reads QUIT. The encryption program reads PASS, ENCRYPT, DECRYPT and QUIT commands from stdin, remembers the current passkey, and prints RESULT or ERROR lines using a Vigenère cipher. The driver is the interactive part because it has a menu, a history of strings, input validation, and it logs every command and result but never logs a password.

My understanding of processes is that each program runs in its own process with its own memory, so they cannot share variables. Starting a child with Popen is the Python version of fork followed by exec. A pipe is a one-way byte stream held in a kernel buffer. The driver holds the write end of the child’s stdin and the read end of its stdout. I think the biggest risk here is buffering. If I write a command and forget to flush, the child will never see it, and then the driver will block it forever on readline, resulting in a deadlock between two processes waiting on each other.

I am using Python because I understand it more than java or C/C++, and it runs on cs1 and cs2 without extra libraries. I considered C with fork, pipe and dup2, but I am not confident I understand it enough to write good code in it and finish that by Friday. 

My overall plan is to do this in 5 sessions. There will be a logger, an encryption program, a driver skeleton, a driver commands implementing code completion, and finally a finishing any remaining code and testing plus readme.

my Plan for this session is to set up the repo and gitignore, write the logger, and test it alone by piping text into it. 
The Goal here is a log file with correctly formatted timestamped lines. 