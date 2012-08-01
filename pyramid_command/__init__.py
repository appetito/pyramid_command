# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime
import inspect

import pyramid.paster
from pyramid.paster import bootstrap
from pyramid.paster import get_appsettings
from pyramid.decorator import reify
from pyramid.path import DottedNameResolver


def _valid_command(obj):
    return inspect.isclass(obj) and issubclass(obj, Command) and obj != Command


class Command(object):
    """base class for console commands"""

    args = tuple()
    description = "no description"
    name = None

    def __init__(self, runner):
        self.runner = runner 
        self.app = runner.bootstrap() # bootstrap application

    def run(self):
        raise NotImplementedError("'run' method of command not implemented")


class CommandRunner(object):
    """
    console application
    """

    def __init__(self, ini_file):
        self.ini_file = ini_file
        self.settings = get_appsettings(ini_file)
        pyramid.paster.setup_logging(ini_file)
        cmd_paths = self.settings.get('console_commands', '').split('\n')
        r = DottedNameResolver()
        cmd_entries = [r.resolve(p.strip()) for p in cmd_paths] 
        self.commands = {}
        for entry in cmd_entries:
            if inspect.ismodule(entry):
                for m in inspect.getmembers(entry, _valid_command):
                    self._register_command(m[1])
            elif _valid_command(entry):
                self._register_command(entry)
            else:
                raise TypeError("Command must be a module or a subclass of 'pyramid_command.Command' class")

    def _register_command(self, cmd):
        if not cmd.name:
            cmd.name = cmd.__name__.lower()
        if cmd.name in self.commands:
            raise TypeError("Command name conflict '%s': %s, %s" % (cmd.name, self.commands[cmd.name], cmd))
        self.commands[cmd.name] = cmd

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
        parser = argparse.ArgumentParser(command.name)
        for a in command.args:
            if isinstance(a[0], (list, tuple)):
                names = a[0]
            else:
                names = (a[0],)
            parser.add_argument(*names, **a[1])
        return parser.parse_args(sys.argv[3:])


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
