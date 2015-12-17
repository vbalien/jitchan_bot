import argparse
import shlex
from plugins.ani_table import ani_table
from plugins.hash import hash_command

outputs = []
plugins = [
    ('애니편성', ani_table),
    ('hash', hash_command),
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
