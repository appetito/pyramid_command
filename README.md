pyramyd_command
===========

Console commands manager for Pyramid framework

usage
======

install package

write your console commands.
for example in myproject.console.py:

    class MyCmd(Command):

        name = "my_cmd"
        description = "My usefull command"

        args = (
                    ("echo", {"help":"echo the string you use here"}),
                    (("-f", "--file"), {"help":"file"}),
                )

        def run(self, echo='dd', file=None):
            print self.name, "runs", echo, file


then configure where to search your commands.
for example in development.ini:
    [app:main]
    use = egg:myproject
    ...
    ...

    console_commands = myproject.console


now run:
    >>>pcommand development.ini my_cmd echoval


