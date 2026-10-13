# 10-13-2026 11:50am
Session 1:
Start Entry:
This is my first entry for the project. I have the basic understanding of the how the project works. The system is basically three separate programs, a logger, an encryption program, and a driver. I only run the driver. It launches the other two as child processes and talks to them through pipes. The logger writes lines like YYYY-MM-DD HH:MM ACTION MESSAGE to a file on the command line, and then stops when it reads QUIT. The encryption program reads PASS, ENCRYPT, DECRYPT and QUIT commands from stdin, remembers the current passkey, and prints RESULT or ERROR lines using a Vigenère cipher. The driver is the interactive part because it has a menu, a history of strings, input validation, and it logs every command and result but never logs a password.

My understanding of processes is that each program runs in its own process with its own memory, so they cannot share variables. Starting a child with Popen is the Python version of fork followed by exec. A pipe is a one-way byte stream held in a kernel buffer. The driver holds the write end of the child’s stdin and the read end of its stdout. I think the biggest risk here is buffering. If I write a command and forget to flush, the child will never see it, and then the driver will block it forever on readline, resulting in a deadlock between two processes waiting on each other.

I am using Python because I understand it more than java or C/C++, and it runs on cs1 and cs2 without extra libraries. I considered C with fork, pipe and dup2, but I am not confident I understand it enough to write good code in it and finish that by Friday. 

My overall plan is to do this in 5 sessions. There will be a logger, an encryption program, a driver skeleton, a driver commands implementing code completion, and finally a finishing any remaining code and testing plus readme.

My Plan for this session is to set up the repo and gitignore, write the logger, and test it alone by piping text into it. 
The Goal here is a log file with correctly formatted timestamped lines. 

During Coding:
The code for this session i am doing is logger.py
- The logger is a separate process with its own file handle, and it only knows what arrives through stdin. It never talks back, so it needs only a one-way pipe.

- It takes the log file name from argv, reads stdin line by line, and writes YYYY-MM-DD HH:MM ACTION MESSAGE lines until it sees QUIT.

- I am putting an edge case, len(sys.argv) != 2 which will throw an error if the arguments are less than the expected count

- The action is the first run of non-whitespace and the rest is the message. Splitting using split(None, 1) keeps the message intact, including its internal spacing.

- i am doing f.flush() after every write because if the driver or logger dies mid-run, lines already logged still reach the disk. It also lets me cat the log while the driver is running to see what is actually happening.

- I was confused on how to open the file but opening in append mode ("a") seemed like the right choice. Running the driver twice doesn’t erase the previous run’s log and that seemed safer than overwriting.

- I did a Uuage check on argv the spec because it says exactly one command line argument, so I fail clearly if it’s missing.

- QUIT is not logged because it’s a control signal for the logger, not a log message. The driver logs its own EXIT line first.

# 10-13-2026 12:55am
Ending entry:
The logger works. It reads lines from stdin, splits off the first word as the action, and writes the timestamped line, stopping on QUIT. I tested it with printf piped into it and the file had the right format. I flushed the file after every write so lines show up immediately, which matters because the driver may crash. This file itself was fairly easy, so I did not encounter any problems. I remembered the flushing concept from UNIX so prevented the unwanted logging problem beforehand. My first version left a trailing space when a message was empty, so I added rstrip.

Next session: I am planning on implementing the encryption program. I want to double check the Vigenère wraparound using the HELLO/HELLO example in the spec, which should give OIWWC. this part should hopefully also be straightforward. 