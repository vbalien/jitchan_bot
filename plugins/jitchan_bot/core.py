import argparse
from plugins.ani_table import ani_table
from plugins.md5 import md5 as hash_md5

outputs = []
plugins = [
    ('애니편성', ani_table),
    ('md5', hash_md5),
]

def process_message(data):
    parser = argparse.ArgumentParser(prog='jitchan_bot')
    parser.add_argument('command', nargs='*')
    print(data)
    if data['text'][:4] != '&gt;':
        return
    data['text'] = data['text'][4:].strip()
    args = parser.parse_args(data['text'].split())

    for plugin in plugins:
        if args.command[0] == plugin[0]:
            plugin[1](data['channel'], args.command, outputs)
