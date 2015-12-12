#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time
import logging
from argparse import ArgumentParser
from xml.sax.saxutils import escape

import telegram

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2


def dbg(debug_string):
    if debug:
        logging.info(debug_string)


class TelegramBot(object):
    def __init__(self, token):
        self.token = token
        self.bot_plugins = []
        self.update_id = None
        self.telegram_client = None
    def connect(self):
        """Convenience method that creates Server instance"""
        self.telegram_client = telegram.Bot(self.token)
        try:
            self.update_id = self.telegram_client.getUpdates()[0].update_id
        except IndexError:
            self.update_id = None
    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            try:
                for reply in self.telegram_client.getUpdates(offset=self.update_id, timeout=10):
                    self.input(reply)
                self.crons()
                self.output()
            except telegram.TelegramError as e:
                # These are network problems with Telegram.
                if e.message in ("Bad Gateway", "Timed out"):
                    time.sleep(.1)
                elif e.message == "Unauthorized":
                    # The user has removed or blocked the bot.
                    update_id += 1
                else:
                    raise e
            except URLError as e:
                # These are network problems on our end.
                time.sleep(.1)
            time.sleep(.1)
    def input(self, update):
        if update.message.text != '':
            function_name = "process_message"
            dbg("got {}".format(function_name))
            data = {}
            data['channel'] = update.message.chat_id
            data['text'] = update.message.text
            if data['text'][0] == '/':
                data['text'] = '>' + data['text'][1:]
            data['text'] = escape(data['text'])
            self.update_id = update.update_id + 1
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)
    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = output[0]
                if channel is not None and output[1] is not None:
                    if limiter == True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('utf-8','ignore')
                    self.telegram_client.sendMessage(chat_id=channel, text="{}".format(message.decode('utf-8')))
                    #channel.send_message("{}".format(message))
                    limiter = True
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
    def load_plugins(self):
        for plugin in glob.glob(directory+'/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory+'/plugins/')
        for plugin in glob.glob(directory+'/plugins/*.py') + glob.glob(directory+'/plugins/*/*.py'):
            logging.info(plugin)
            name = plugin.split('/')[-1][:-3]
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugin %s" % name


class Plugin(object):
    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in config:
            logging.info("config found for: " + name)
            self.module.config = config[name]
        if 'setup' in dir(self.module):
            self.module.setup()
    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            logging.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []
    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")
    def do_jobs(self):
        for job in self.jobs:
            job.check()
    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output


class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass


class UnknownChannel(Exception):
    pass


def main_loop():
    if "LOGFILE" in config:
        logging.basicConfig(filename=config["LOGFILE"], level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    config = yaml.load(open(args.config or 'rtmbot.conf', 'r'))
    debug = config["DEBUG"]
    bot = TelegramBot(config["TELEGRAM_TOKEN"])
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    if "DAEMON" in config:
        if config["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop()
    main_loop()
