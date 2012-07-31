# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime

import pyramid.paster
from pyramid.paster import bootstrap
from pyramid.paster import get_appsettings
from pyramid.decorator import reify
from pyramid.path import DottedNameResolver


class CommandRunner(object):
    """
    console application
    """

    def __init__(self, ini_file):
        self.ini_file = ini_file
        self.settings = get_appsettings(ini_file)
        pyramid.paster.setup_logging(ini_file)
        cmd_list = self.settings.get('console_commands', '').split('\n')
        r = DottedNameResolver()
        self.commands = {}
        for cmd in cmd_list:
            cmd_class = r.resolve(cmd)
            self.commands[cmd_class.name] = cmd_class

    def bootstrap(self):
        return bootstrap(self.ini_file)

    def run(self, command):
        if command not in self.commands:
            print "available commands: "
            for name, cmd in self.commands.items():
                print '\t* ', '%s: %s' %(name, cmd.description)
            return
        cmd = self.commands[command]
        args = self.parse_args(cmd)
        cmd(self).run(**vars(args))

    def parse_args(self, command):
        parser = argparse.ArgumentParser(command.description)
        for a in command.args:
            if isinstance(a[0], (list, tuple)):
                names = a[0]
            else:
                names = (a[0],)
            parser.add_argument(*names, **a[1])
        return parser.parse_args(sys.argv[3:])


class Command(object):
    """base class for console commands"""

    args = tuple()

    def __init__(self, runner):
        self.runner = runner # bootstrap application
        self.app = runner.bootstrap()

    def run(self):
        raise NotImplementedError("'run' method of command not implemented")



class Migrate(Command):
    name = u'migrate'
    description = u'Migrate database schema'

    args = (
            (('--silent', '-s'), {'help': 'no output', 'dest':'silent', 'action': 'store_true'}),
            ('--script', {'help': 'execute SQL script', 'dest':'script'}),
        )



def main():
    usage = 'Usage: %s settings_file.ini command' %(os.path.basename(sys.argv[0]))

    if len(sys.argv) < 2:
        print usage
        sys.exit(1)

    ini_file = os.path.abspath(sys.argv[1])

    if not os.path.isfile(ini_file):
        print 'No settings file %s' %(ini_file)
        print usage
        sys.exit(1)

    runner = CommandRunner(ini_file)
    try:
        command = sys.argv[2]
    except IndexError:
        command = ''

    runner.run(command)

if __name__ == '__main__':
    main()
