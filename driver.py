import os
import sys
from subprocess import Popen, PIPE

def script_path(name):
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

def log(logger, action, msg=""):
  logger.stdin.write(f"{action} {msg}\n")
  logger.stdin.flush()

def send(enc, cmd):
  enc.stdin.write(cmd + "\n")
  enc.stdin.flush()
  return enc.stdout.readline().rstrip("\n")

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