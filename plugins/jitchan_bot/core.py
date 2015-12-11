import argparse
from ani_table import ani_table

outputs = []
plugins = []
plugins.append(
    ('애니편성', ani_table)
)

def process_message(data):
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('command', nargs='*')
    args = parser.parse_args(data['text'].split())
    if args.command[0][:4] != '&gt;':
        return
    args.command[0] = args.command[0][4:].strip()

    for plugin in plugins:
        if args.command[0] == plugin[0]:
            plugin[1](data['channel'], args.command, outputs)
