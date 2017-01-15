import cmd

import TCX
import activities

class justletic(cmd.Cmd):

    """ Command Line Interface for Justletic

    """

    # Session variables
    activity = None

    def do_load(self,line):
        """Usage: load filename
        Load the activity from the TCX file filename to the session"""
        args = line.split()

        if len(args) != 1:
            self.default("Usage: load filename")
        else:
            self.activity = activities.run(TCX.parse(args[0]))

    def do_print(self,line):
        """Usage: print [num_samples]
        Print "num_samples" of current activity"""
        args = line.split()

        if self.activity is None:
            print("No activity loaded")
        elif len(args) == 0:
            self.activity.print()
        elif len(args) == 1:
            self.activity.print(int(args[0]))
        else:
            self.default("Usage: print [num_samples]")

    def do_quit(self,line):
        """ Quit Justletic"""
        return True

    def emptyline(self):
        pass




if __name__ == "__main__":
    je = justletic()
    je.prompt = ">>>"
    je.cmdloop()
