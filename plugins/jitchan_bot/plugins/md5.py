import hashlib

def md5(peer, command, outputs):
    msg = hashlib.md5(command[1].encode()).hexdigest()
    outputs.append([peer, msg])
