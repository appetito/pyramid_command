pyramyd_command
===========

Console commands manager for Pyramid framework

usage
======

install package

Write your console commands.
For example in myproject/console.py:

    from pyramid_command import Command
    
    class MyCmd(Command):

        name = "my_cmd"
        description = "My usefull command"

        args = (
                    ("echo", {"help":"echo the string you use here"}),
                    (("-f", "--file"), {"help":"file"}),
                )

        def run(self, echo='dd', file=None):
            print self.name, "runs", echo, file


Then configure where to search your commands.
For example in development.ini:

        [app:main]
        use = egg:myproject
        ...
        ...
        console_commands = myproject.console


Now run:

    >>>pcommand development.ini my_cmd echoval


