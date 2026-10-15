import sys

key = None 

def vig(text, key, sign):
  out, k = [], 0

  for ch in text:
    shift = ord(key[k % len(key)]) - 65
    out.append(chr((ord(ch) - 65 + sign * shift) % 26 + 65))
    k += 1
  return "".join(out)

def valid(s):
  return s.isascii() and s.isalpha()

def reply(s):
  print(s)
  sys.stdout.flush()

while (True):
  line = sys.stdin.readline()

  if not line:
    break

  parts = line.rstrip("\n").split(" ", 1)
  cmd = parts[0]
  arg = parts[1].strip().upper() if len(parts) > 1 else ""

  if cmd == "QUIT":
    break
  elif cmd == "PASS":
    if valid(arg):
      key = arg
      reply("RESULT")
    else:
      reply("ERROR Passkey must contain only letters")
  elif cmd in ("ENCRYPT", "DECRYPT"):
    if key is None:
      reply("ERROR Passkey not set")
    elif not valid(arg):
      reply("ERROR Input must contain only letters")
    else:
      reply("RESULT " + vig(arg, key, 1 if cmd == "ENCRYPT" else -1))
  else:
    reply("ERROR Unknown command")

