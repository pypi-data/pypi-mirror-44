import os
import re

from .file_mgr import copy_file, get_name, get_div, get_version, sep_block
from .scripts import run
from . import __version__


# main update function
def update(filename, template_type):
    ver = get_version(filename)
    if not os.path.exists(filename):
        print("Error: No file named \"{}\" to update!".format(filename))
    elif ver.startswith("0."):
        print("Error: File too outdated! Must be generated with version at least 1.0; file version is ({})".format(ver))
    else:
        # copy the file to a new location
        name = get_name(filename,"_old")
        os.rename(filename,name)

        # read contents of file to user dict by separating relevant blocks
        with open(name,'r') as f:
            fl = list(f)
        macros = sep_block(fl,"file-specific macros")
        body = sep_block(fl,"document start")

        # strip last item of macros to avoid increasing whitespace in file
        if len(macros) >= 1:
            macros[-1] = macros[-1].rstrip()

        # rebuild file
        user = {'macros':macros,'contents':body}
        run(filename, template_type, user_macros=user)
