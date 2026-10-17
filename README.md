# CS4348 Project 1

## Files

### `devlog.md`

1. This file is the development journal for the project.
2. It records notes from the author's project sessions.
3. Entries describe plans made before implementation work.
4. They also reflect on progress made during each session.
5. The journal explains the intended roles of the three programs.
6. It describes how the driver launches the other processes.
7. It records how the programs communicate through pipes.
8. It discusses why input and output buffering matters.
9. It outlines the logger's input and output behavior.
10. It records the planned commands for the encryption process.
11. It explains the Vigenere cipher implementation approach.
12. It notes why input validation restricts text to ASCII letters.
13. It includes implementation decisions and their rationale.
14. It records testing ideas and observations as work progresses.
15. It is documentation only and is not required to run the program.

### `logger.py`

1. This file implements the program's logging worker process.
2. The driver starts it as a child process.
3. It expects one command-line argument: the log file path.
4. It prints a usage message and exits if the argument is missing.
5. It reads logging instructions from standard input.
6. Each non-empty instruction begins with an action name.
7. Any remaining text on that line becomes the log message.
8. It stops reading when it receives the `QUIT` action.
9. The `QUIT` control instruction itself is not written to the log.
10. For other actions, it obtains the current date and time.
11. It formats the timestamp as year-month-day and hour:minute.
12. It writes the timestamp, action, and message as one record.
13. It opens the log file in append mode to preserve existing entries.
14. It flushes the file after each record so entries are written promptly.
15. It runs separately from the driver and does not send replies.

### `encrypt.py`

1. This file implements the encryption and decryption worker process.
2. The driver starts it as a child process without a log-file argument.
3. It reads one command at a time from standard input.
4. It exits when it receives `QUIT` or reaches end-of-input.
5. It stores the active password in memory as process state.
6. The `PASS` command sets that password after validation.
7. Passwords must contain ASCII letters only.
8. `ENCRYPT` and `DECRYPT` commands process the supplied string.
9. Those input strings must also contain ASCII letters only.
10. Valid inputs are normalized to uppercase before processing.
11. The cipher uses the Vigenere method with the password as its key.
12. The key repeats to provide a shift for each input letter.
13. Encryption shifts letters forward through the alphabet.
14. Decryption shifts letters backward through the alphabet.
15. It writes a `RESULT` or `ERROR` response for each handled command.

### `driver.py`

1. This file is the interactive entry point for the program.
2. The user runs it with the log-file path as its sole argument.
3. It displays the menu and reads commands from the user.
4. The menu supports `password`, `encrypt`, `decrypt`, `history`, and `quit`.
5. It normalizes menu commands to lowercase.
6. It validates entered passwords and strings as ASCII letters.
7. It starts `encrypt.py` and `logger.py` as child processes.
8. It communicates with the encryption process using standard-input and output pipes.
9. It flushes commands to the child and reads its response.
10. It displays encryption results and error responses to the user.
11. It keeps string history in memory for the current run only.
12. For encryption and decryption, it can offer strings from that history.
13. It asks the logger process to record commands, inputs, results, and errors.
14. It does not send passwords to the logger or store them in string history.
15. When quitting, it tells both child processes to stop and waits for them to exit.

## How to run

From the project directory, run:

```bash
python3 driver.py logfile.log
```

Replace `logfile.log` with the path you want to use for the activity log.

## Menu commands

- `password` — enter the password used as the cipher key.
- `encrypt` — encrypt a string.
- `decrypt` — decrypt a string.
- `history` — view strings kept during the current run.
- `quit` — exit the program.

## Notes for the TA

- Passwords and strings must contain letters only (A-Z); input is case insensitive.
- String history lasts only for one run.
- Passwords are never logged or stored in history.
- The log file is appended to if it already exists.
