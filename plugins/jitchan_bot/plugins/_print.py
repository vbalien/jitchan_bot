def print_command(peer, command, outputs):
    for i in command[1:]:
        outputs.append([peer, i])
