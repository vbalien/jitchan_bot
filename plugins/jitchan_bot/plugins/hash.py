import hashlib

def hash_command(peer, command, outputs):
    hash_algos = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
    }
    if command[1] in hash_algos:
        msg = hash_algos[command[1]](command[2].encode()).hexdigest()
        outputs.append([peer, msg])
