saveload_data = ''

def save_command(peer, command, outputs):
    global saveload_data
    saveload_data = command[1]
    outputs.append([peer, '저장하였습니다!'])


def load_command(peer, command, outputs):
    global saveload_data
    outputs.append([peer, saveload_data])
