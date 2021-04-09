from subprocess import PIPE, Popen
from typing import Tuple

def cmdline(command:str) -> Tuple:
    process = Popen(
        args=command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    )
    return (process.communicate()[0],process.communicate()[1], process.returncode)

def error_out(response:Tuple):
    if response[2] != 0:
        print(f"An error occured: \n     {response[1]}")
        exit(1)
