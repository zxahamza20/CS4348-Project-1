import sys
from datetime import datetime

def main():
  if len(sys.argv) != 2:
    sys.stderr.write("Usage: logger.py LOGFILE\n")
    sys.exit(1)

  with open(sys.argv[1], 'a') as f:
    for line in sys.stdin:
      line = line.strip()

      if not line:
        continue

      parts = line.split(None, 1)
      action = parts[0]

      if action == "QUIT":
        break

      msg = parts[1] if len(parts) > 1 else ""

      stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

      f.write(f"{stamp} [{action}] {msg}".rstrip() + "\n")

      f.flush()

main()