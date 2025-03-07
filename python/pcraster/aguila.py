import os
import subprocess
import threading
import pcraster


class AguilaThread(threading.Thread):

    def __init__(self,
            *arguments,
            **keywords):
        threading.Thread.__init__(self)
        self.arguments = arguments
        self.keywords = keywords
        self.created_files_names = []

    def __del__(self):
        # Get rid of any files we created.
        for filename in self.created_files_names:
            os.remove(filename)

    def parse_arguments(self,
            arguments):
        argument_list = []
        for argument in arguments:
            assert isinstance(argument, (str, list,
                pcraster._PCRaster.Field)), "{} has type {}".format(argument,
                    type(argument))

            if isinstance(argument, str):
                argument_list.append(argument)
            elif isinstance(argument, list):
                argument_list.append(" + ".join(self.parse_arguments(argument)))
            elif isinstance(argument, pcraster._PCRaster.Field):
                temp_name = os.tmpnam()
                pcraster.report(argument, temp_name)
                self.created_files_names.append(temp_name)
                argument_list.append(temp_name)

        return argument_list

    def run(self):
        argument_list = self.parse_arguments(self.arguments)
        command = "aguila {}".format(" ".join(argument_list))
        subprocess.call(command, shell=True)


def aguila(
        *arguments,
        **keywords):
    thread = AguilaThread(*arguments, **keywords)
    thread.start()
    # Don't join. Just return to the caller.
    # thread.join()
