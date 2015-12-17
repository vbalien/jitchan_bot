import argparse
import shlex
from plugins.ani_table import ani_table
from plugins.hash import hash_command
from plugins._print import print_command
from plugins.saveload import save_command, load_command

config = {}
outputs = []
plugins = [
    ('애니편성', ani_table), ('애니편성표', ani_table), ('애니', ani_table),
    ('hash', hash_command),
    ('출력', print_command),
    ('저장', save_command),
    ('불러', load_command),
]

def process_message(data):
    parser = argparse.ArgumentParser(prog='jitchan_bot')
    parser.add_argument('command', nargs='*')

    if data['text'][:4] != '&gt;':
        return
    data['text'] = data['text'][4:].strip().replace('“', '"').replace('”', '"')
    args = parser.parse_args(shlex.split(data['text']))

    for plugin in plugins:
        if args.command[0] == plugin[0]:
            plugin[1](data['channel'], args.command, outputs)
