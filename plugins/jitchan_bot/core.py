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

    if data['text'][:4] != '&gt;':
        return
    data['text'] = data['text'][4:].strip()
    args = parser.parse_args(data['text'].split())

    for plugin in plugins:
        if args.command[0] == plugin[0]:
            plugin[1](data['channel'], args.command, outputs)
