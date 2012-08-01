from pyramid_command import Command

class Cmd1(Command):

    name = 'com1'

    def run(self):
        print self.name, "runs"


class Cmd2(Command):

    description = "Commm"

    args = (
                ("echo", {"help":"echo the string you use here"}),
                (("-f", "--file"), {"help":"file"}),
            )

    def run(self, echo='dd', file=None):
        print self.name, "runs", echo, file