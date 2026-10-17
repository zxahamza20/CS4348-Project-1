# 10-13-2026 11:50am
Session 1:
Start Entry:
This is my first entry for the project. I have the basic understanding of the how the project works. The system is basically three separate programs, a logger, an encryption program, and a driver. I only run the driver. It launches the other two as child processes and talks to them through pipes. The logger writes lines like YYYY-MM-DD HH:MM ACTION MESSAGE to a file on the command line, and then stops when it reads QUIT. The encryption program reads PASS, ENCRYPT, DECRYPT and QUIT commands from stdin, remembers the current passkey, and prints RESULT or ERROR lines using a Vigenère cipher. The driver is the interactive part because it has a menu, a history of strings, input validation, and it logs every command and result but never logs a password.

My understanding of processes is that each program runs in its own process with its own memory, so they cannot share variables. Starting a child with Popen is the Python version of fork followed by exec. A pipe is a one-way byte stream held in a kernel buffer. The driver holds the write end of the child’s stdin and the read end of its stdout. I think the biggest risk here is buffering. If I write a command and forget to flush, the child will never see it, and then the driver will block it forever on readline, resulting in a deadlock between two processes waiting on each other.

I am using Python because I understand it more than java or C/C++, and it runs on cs1 and cs2 without extra libraries. I considered C with fork, pipe and dup2, but I am not confident I understand it enough to write good code in it and finish that by Friday. 

My overall plan is to do this in 5 sessions. There will be a logger, an encryption program, a driver skeleton, a driver commands implementing code completion, and finally a finishing any remaining code and testing plus readme.

My Plan for this session is to set up the repo and gitignore, write the logger, and test it alone by piping text into it. 
The Goal here is a log file with correctly formatted timestamped lines. 

Coding session starts:
The code for this session i am doing is logger.py
- The logger is a separate process with its own file handle, and it only knows what arrives through stdin. It never talks back, so it needs only a one-way pipe.

- It takes the log file name from argv, reads stdin line by line, and writes YYYY-MM-DD HH:MM ACTION MESSAGE lines until it sees QUIT.

- I am putting an edge case, len(sys.argv) != 2 which will throw an error if the arguments are less than the expected count

- The action is the first run of non-whitespace and the rest is the message. Splitting using split(None, 1) keeps the message intact, including its internal spacing.

- i am doing f.flush() after every write because if the driver or logger dies mid-run, lines already logged still reach the disk. It also lets me cat the log while the driver is running to see what is actually happening.

- I was confused on how to open the file but opening in append mode ("a") seemed like the right choice. Running the driver twice doesn’t erase the previous run’s log and that seemed safer than overwriting.

- I did a Uuage check on argv the spec because it says exactly one command line argument, so I fail clearly if it’s missing.

- QUIT is not logged because it’s a control signal for the logger, not a log message. The driver logs its own EXIT line first.

# 10-13-2026 12:55pm
Ending entry:
The logger works. It reads lines from stdin, splits off the first word as the action, and writes the timestamped line, stopping on QUIT. I tested it with printf piped into it and the file had the right format. I flushed the file after every write so lines show up immediately, which matters because the driver may crash. This file itself was fairly easy, so I did not encounter any problems. I remembered the flushing concept from UNIX so prevented the unwanted logging problem beforehand. My first version left a trailing space when a message was empty, so I added rstrip.

Next session: I am planning on implementing the encryption program. I want to double check the Vigenère wraparound using the HELLO/HELLO example in the spec, which should give OIWWC. this part should hopefully also be straightforward. 

# 10-15-2026 1:36pm
Session 2:
Start Entry:
Thoughts since last session: The encryption program follows the same structure as the logger, as in it reads lines until QUIT, with two differences. First, it has to write a reply to stdout for every command, and the driver will block on readline() waiting for exactly one reply line. If I ever skip a reply or forget to flush it, the driver hangs. Second, it has to remember state, because the passkey must persist across commands. Since it’s a long-running process, a global variable that starts as None works. A None key is how I will detect that no password has been set.

Plan for this session: write encrypt.py with PASS, ENCRYPT, DECRYPT, QUIT, plus ERROR replies for an unset key, non-letter input and unknown commands.

My Vigenère plan: convert each letter to 0 through 25 with ord(ch), add the matching key letter’s value, take mod 26, and convert back. For decryption I subtract instead of add. The key repeats, so the key position is the character index mod the key length. I’ll use one function with a sign parameter instead of two copies so the two directions can’t drift apart. Python’s modulo returns a non-negative number for negatives, so the decrypt wraparound should work without special cases.

Input validation: I’ll use isalpha() and also isascii(), because Python’s isalpha() accepts letters like “é”, and that would break the 0 to 25 math.

Testing plan: I will use printf to send commands, check the spec example, and check that decrypting an encrypted string gives the original.

Coding session starts:
The code I am doing for this sesison is in a file encrypt.py
- It reads commands from stdin, keeps the passkey in a global, and replies with RESULT or ERROR lines.

- I made key = None a global state because the spec says the encryption program remembers the key between commands. None lets me distinguish “never set” and produce the “Password not set” error.

- .upper() on the argument seems fair because the cipher is case insensitive. Normalizing here means the backend works even if the driver forgets.

- I am planning on using one vig() function with a sign parameter. Encrypt adds the key shift and decrypt subtracts it. Using one function avoids two near-identical copies that could drift apart.

- I dont really know how this will work in code. I was thinking somehing like:
out.append(chr((ord(ch) - 65 + sign * shift) % 26 + 65))
  - This line performs the mathematical core of the Vigenère cipher: it takes an uppercase ASCII letter ch, shifts it forward (encryption) or backward (decryption) by shift positions within the 26-letter alphabet, and appends the transformed character to the output list out.

- Key index advances per character (k) so the key repeats across the plaintext. Every character is a letter because I validate first, so I don’t need to worry about skipping spaces.

- valid() using isascii() and isalpha() because python’s isalpha() accepts accented letters like “é”, which would break the ord(ch) - 65 math. Requiring ASCII fixes that.

- PASS replies a bare RESULT because the spec’s example shows Output: RESULT for PASS.

- Unknown command returns ERROR instead of crashing because a backend should never die because of malformed input.

My first test appeared to hang. I realized I was printing without flushing, and since stdout was a pipe, Python buffered it. This is exactly the problem I expected in session 1, and now I understand why the driver will need the same care.

- I am using a reply() helper that prints and flushes. The driver blocks on readline(), waiting for exactly one reply per command. When stdout is a pipe, Python buffers output instead of sending it, so without a flush the driver would hang. The helper means I can’t forget it.

To test this file raw: 
printf 'ENCRYPT HELLO\nPASS HELLO\nENCRYPT HELLO\nDECRYPT OIWWC\nQUIT\n' | python3 encrypt.py

# 10-15-2026 3:17pm
End Entry:
The encryption program works. Running printf 'ENCRYPT HELLO\nPASS HELLO\nENCRYPT HELLO\nDECRYPT OIWWC\nQUIT\n' | python3 encrypt.py printed ERROR Password not set, RESULT, RESULT OIWWC and RESULT HELLO. it verified that all the cases in the code worked fine in the terminal. 

I made the passkey live in a global variable because the process needs to remember it. The reply() helper flushes every response because a buffered reply would deadlock the driver. I put validation in the encryptor even though the driver will validate too, because a backend should not trust its caller A backend service should never trust its caller because relying on the client to sanitize input breaks the security boundary of an isolated process or service. 

What this shows about pipes and processes is that the key exists only inside this process’s memory. The driver can never read it directly. It can only send a command and read the reply, which is why a clear line-based protocol matters.

The only problem I encountered this session was that I was printing without flushing so the program kept getting hanged.I made a replay helper function which replied and then flusherd to remedy this issue.

Next session, I will build the driver skeleton, which is the first time all three processes will run together. I will will only implement the quit functionality for now because I more time to figure out how to tie all of this together in a single main entry point. 

# 10-16-2026 1:32am
Session 3:
Start Entry:
Since last session I realized both child programs work on their own, so any bug I see from now on will be most likely in the connection between them. That’s why I’m splitting the driver across three sessions and building the plumbing first, before any menu features. If the processes can start, exchange a message and shut down cleanly, everything after that is just adding commands on top.

The key design question is how many pipes each child needs. The logger only receives text. It never talks back, so it needs one pipe (the driver writes to the logger’s stdin). The encryption program receives commands and sends replies, so it needs two pipes, one in each direction. I’ll create exactly those with stdin=PIPE and stdout=PIPE and not open any pipe I don’t use. I’ll also pass encoding="utf8", so the pipes behave like text streams and I can use readline().

I’ll launch the children with sys.executable instead of the string "python". That way the children always use the same interpreter as the driver, and it works whether the machine calls it python or python3. 

I’ll build the child paths from __file__ so the driver finds logger.py and encrypt.py even if I run it from a different directory.
I’ll write two helpers. send() writes one line to the encryptor, flushes, and reads exactly one line of reply. log() writes one line to the logger and flushes. Using helpers means every message follows the same pattern, and I only have to get the flush right once.

For the shutdown order, I need to tell the encryptor to quit, log my own EXIT line while the logger is still alive, tell the logger to quit, close both pipes, then wait for both children. If I logged EXIT after quitting the logger, I’d be writing into a pipe nobody reads.
EOFError from input() (Ctrl-D) will count as quit, so the program doesn’t crash with a traceback.

My plan for this session is to write only the skeleton, with quit as the only working command and a placeholder for everything else. Success means running it, typing quit, and finding START, COMMAND and EXIT lines in the log file with both children gone.

Coding session starts:
The code I am doing for this session is the skeleton and a small functionality in driver.py which connects logger and encrypter into a single point, basically this is where the prohram is run, it is the entry point. As of right now, it starts the logger and encryptor as child processes, connects them with pipes, runs a menu loop where only quit works, then shuts everything down cleanly.

- I used Popen with PIPE because this is the Python version of fork, pipe, dup2 and exec combined, and it’s the subprocess module the spec requires. 

- in total I am using 3 pipes, one pipe for the logger, two for the encryptor. The logger only receives text, so stdin=PIPE is enough. The encryptor receives commands and sends replies, so it needs stdin=PIPE and stdout=PIPE. I didn’t open a pipe I wouldn’t read, because an unread pipe can fill up and block the child.

- I think I want to use encoding="utf8" because pipes carry raw bytes by default. This makes them behave as text, so I can write strings and call readline() directly.

- I built the script_path() from __file__ because the driver finds logger.py and encrypt.py next to itself, even if I launch it from another directory.

- send() helper (write, flush, readline): each command gets exactly one reply line, so requests and replies stay paired. The flush is essential, because buffered data never reaches the child, and then the driver blocks forever waiting for a reply.

- log() helper: every log message goes through one function with one flush, so I only have to get it right once.

- Shutdown order serves a few purposes for example send QUIT to the encryptor, log EXIT while the logger is still alive, send QUIT to the logger, close both pipes, then wait() on both. Logging EXIT after the logger quit would write into a dead pipe.

- I am closing pipes before wait(). Closing stdin guarantees the child sees EOF even if it missed QUIT. wait() collects the exit status so no zombie processes remain.

- EOFError treated as quit and Ctrl-D makes input() raise an exception. Catching it gives a clean exit instead of a traceback.

- Placeholder branch (“Not implemented yet”) lets me test the plumbing before adding features. If something breaks later, I know the pipes already worked.

The main concepts I am using here are parent and child processes, separate memory, why pipes are one-way (so two-way talk needs two pipes), and how a missing flush can deadlock both sides.

I noticed the driver never reads from the logger, so I didn’t create a stdout pipe for it. An unread pipe can fill up and block the child.

I found 2 errors:
The driver hung at exit the first time. I had sent QUIT to the logger but never closed the pipe or called wait(). Closing stdin guarantees the child sees EOF even if it missed QUIT, and wait() collects the child’s exit status so it doesn’t linger as a zombie process.

My log lines were missing at first. I forgot the flush in log(), so the data was sitting in Python’s buffer and the logger never received it.

# 10-16-2026 3:37am
End entry:
looking back on this session, the skeleton works just fine. I ran python3 driver.py t.log, typed quit, and the log contained START, COMMAND and EXIT lines with correct timestamps. The prompt returned immediately and ps showed no leftover python processes”. pressing quit immediately terminated everything and brought me back to the root directory. 

Using Popen with PIPE is how I satisfy the spec’s use of the subprocess module. It does what fork, pipe, dup2 and exec would do in C: create a child process and connect its standard streams to pipes the parent holds. The helpers keep the request and reply pattern consistent, and the shutdown order avoids writing to a closed logger.

I understand better now that a pipe is one-way, so a two-way conversation needs two pipes. Messages have to pair up one request to one reply. If the driver waits for a reply the child never sends, both sides wait forever. and potentially enter a deadlock. 

In the next session, I will build and add the history, string validation, and the password and encrypt commands to give the program more functionality and remove the "not yet implemented" line.

# 10-16-2026 2:43pm
Session 4:
Start Entry:
Some thoughts I had since last session: The pipes are confirmed to be working, so this session is about the user-facing behavior. The spec describes the same “history or new string” flow for password, encrypt and decrypt, so I’m going to write one choose() function and reuse it, rather than duplicating the logic and risking any inconsistencies.

For exiting the history, the spec requires a way out of the history menu to enter a new string. I’ll use 0 for that, because the valid choices start at 1 and can’t collide with it and for empty history I will skip the “use history?” question entirely. I will validate before storing, so bad input never reaches history. 
For logging, for each command I log the command, then the input, then the result or error. For passwords I log only “Password set”, never the value, because passwords are never directly logged.
For results into history, the encryptor replies RESULT OIWWC, and I strip the RESULT prefix so history holds just the text, which makes it usable as input for a later command.


My plan for this session is to write choose() and show_history(), add the history command, then password, then encrypt, testing each by hand before moving on. I’m deliberately leaving decrypt for the next session so I can see whether encrypt and decrypt end up being nearly identical.

Coding session starts:
The code I am doing for this session is the history, choose(),password, and encrypt part of code for the driver.py file. These add the history list, a shared function for getting a string from the user, and the history, password and encrypt commands.

- I used history as a module-level list because the spec says history lasts only for the current run, so memory is enough and No file is needed.

- I have one choose() function because again, the spec describes the same “history or new string” flow for password, encrypt and decrypt. Writing it once keeps validation and the history menu consistent, and means a bug only has to be fixed in one place.

- I have a store flag because passwords must never be saved in history, but encrypt and decrypt inputs must, so one parameter covers both these cases.

- Option 0 leaves the history menu. The spec requires a way out of the history to enter a new string. Valid choices start at 1, so 0 will not collide with a real one.

_ I decided skipping the “use history?” question when it’s empty because it would be pointless and confusing.

- I need both isascii() plus isalpha()\ because isalpha() alone accepts letters like “é”, which would break the backend’s ord(ch) - 65 math. This is why I validate more strictly than the obvious check.

Another seemingly trivial decision but a big error avoider decision I made was to validate before storing. Invalid input like Hello World! is rejected before it can reach the history.

- The calling command logs an error and goes back to the menu. This is simpler than looping forever and it also satisfies the spec’s error checking requirement.

- Password handling is an important securty issue I am taking care of. The driver logs only “Password set”, never the value, and it also isn’t added to history.

- Because results are saved to be reused as input I am puttinh them in the history. I strip "RESULT " so only the text is stored.

- PASS replies a bare RESULT while ENCRYPT replies RESULT text. A prefix check handles both, and anything else is logged as an error.

- I decided on Logging the command, the input and the result separately. This makes a readable audit trail.

- Validation in both the driver and the encryptor means the driver gives the user fast feedback and a clean log. The encryptor still checks, because a backend shouldn’t trust its caller.

I wanted to see whether encrypt and decrypt would turn out identical before writing a second copy so I am deferring decrypt to the last session: 

The concepts I was conciously aware of here are that the driver is a controller that translates user actions into the pipe protocol. It owns user-facing state, history. The encryptor owns only the passkey, and the logger owns only the file.

I tested choose() first with only the history command so I could check the menu before involving the encryptor.

Some tradeoffs of my previous code were that I originally appended the string to history before validating, so a bad string like Hello World! landed in the history. I moved the check to happen first.

I stored the entire reply RESULT OIWWC in history instead of just the text, so choosing it as input failed validation. I strip the prefix now.

Also, after choosing from history, I noticed it wasn’t re-added to history. I decided that’s right, because it’s already in there.

# 10-16-2026 4:48pm
End entry:
Current status of the project is that password, encrypt and history work. After a test run, password HELLO gives RESULT, encrypt HELLO gives RESULT OIWWC, history shows HELLO and OIWWC, and encrypting Hello World! gives an error and adds nothing to the history. The log contains the command, input and result lines, and no password.

I basically made one shared choose() which keeps validation and the history menu consistent. The store flag keeps passwords out of history. Validating in the driver as well as in the encryptor gives quick feedback to the user and a clean log, while the backend still protects itself.

I think I understand better now that the driver is a controller. It owns user-facing state like the history, the encryptor owns only the passkey, and the logger owns only the file. Each process has one job, and the pipes carry the messages between them.

For the next session: I only have one more thing to add, decrypt. The encrypt branch looks like it can be shared with decrypt almost unchanged. After that, final testing, and the reademe, which will be the end. 

# 10-16-2026
Session 5:
Start entry:
Since the last session, I realized that since encrypt works, and looking at the code again, decrypt would be identical except for the command word. Writing a second copy would double the places a bug could hide, so I’ll merge them into one branch driven by the command name. I’ll also add proper handling for unknown commands, which currently print a placeholder.

The things I’ll check against the spec are log format, action as first word, no passwords in the log or history, history exit option, letters-only checks, case insensitivity, and the logging of start and exit.

My plan for this session is to merge encrypt and decrypt into one branch, and log unknown commands. ALong with that, run the full test checklist, including a grep of the log for the test password and fix anything that fails along with writing the README.
