from pyramid_command import Command

class Cmd(Command):

    name = 'cmd'

    def run(self):
        print "Cmd run"