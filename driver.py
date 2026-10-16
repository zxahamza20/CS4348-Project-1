import os
import sys
from subprocess import Popen, PIPE

history = []

def script_path(name):
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

def log(logger, action, msg=""):
  logger.stdin.write(f"{action} {msg}\n")
  logger.stdin.flush()

def send(enc, cmd):
  enc.stdin.write(cmd + "\n")
  enc.stdin.flush()
  return enc.stdout.readline().rstrip("\n")

def show_history():
  for i, h in enumerate(history, 1):
    print(f"  {i}. {h}")

def choose(label, store):
  use_hist = False
  if history:
    use_hist = input("Use a string from history? (y/n): ").strip().lower() == "y"

  while True:
    if use_hist:
      show_history()
      sel = input("Number (0 = enter a new string instead): ").strip()
      if sel.isdigit() and 1 <= int(sel) <= len(history):
        return history[int(sel) - 1]
      if sel == "0":
        use_hist = False
        continue
      print("Invalid selection.")
      continue
    s = input(f"Enter {label}: ").strip()
    if s.isascii() and s.isalpha():
      s = s.upper()
      if store:
        history.append(s)
      return s
    print("Error: letters only (A-Z).")
    return None
    


def main():
  if len(sys.argv) != 2:
    sys.stderr.write("Usage: driver.py LOGFILE\n")
    sys.exit(1)

  logger = Popen([sys.executable, script_path("logger.py"), sys.argv[1]],stdin=PIPE, encoding="utf8")

  enc = Popen([sys.executable, script_path("encrypt.py")], stdin=PIPE, stdout=PIPE, encoding="utf8")

  log(logger, "START", "Driver started.")

  while True:
    print("\nCommands: password, encrypt, decrypt, history, quit")
    try:
      cmd = input("> ").strip().lower()
    except EOFError:
      cmd = "quit"
    if cmd == "quit":
      log(logger, "COMMAND", "quit")
      break
    elif cmd == "history":
      log(logger, "COMMAND", "history")
      if history:
        show_history()
      else:
        print("History is empty.")
    elif cmd == "password":
      log(logger, "COMMAND", "password")
      s = choose("password", False)
      if s is None:
        log(logger, "ERROR", "Invalid password input")
        continue
      resp = send(enc, "PASS " + s)
      print(resp)
      log(logger, "RESULT", "Password set" if resp.startswith("RESULT") else resp)
    elif cmd == "encrypt":
      log(logger, "COMMAND", "encrypt")
      s = choose("string to encrypt", True)
      if s is None:
        log(logger, "ERROR", "Invalid input string")
        continue
      log(logger, "INPUT", s)
      resp = send(enc, "ENCRYPT " + s)
      print(resp)
      if resp.startswith("RESULT "):
        history.append(resp[7:])
        log(logger, "RESULT", resp[7:])
      else:
        log(logger, "ERROR", resp)
    else:
      print("Not implemented yet.")

  enc.stdin.write("QUIT\n")
  enc.stdin.flush()
  log(logger, "EXIT", "Driver exiting.")
  logger.stdin.write("QUIT\n")
  logger.stdin.flush()
  enc.stdin.close()
  logger.stdin.close()
  enc.wait()
  logger.wait()

main()