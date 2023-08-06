import sys

from .template import build, update, load_template, load_user, available_templates
from .document import TexnewDocument
from .rpath import safe_rename, RPath
from pathlib import Path

def run(fname, template_type):
    """Make a LaTeX file fname from template name template_type"""
    # load and catch basic errors with template choice
    fpath = Path(fname)
    if fpath.exists():
        print("Error: The file \"{}\" already exists. Please choose another filename.".format(fname))
        sys.exit(1)

    try:
        user_info = load_user()
    except FileNotFoundError:
        print("Warning: no user file found, no substitutions will be made!")
        user_info = {}

    try:
        template_data = load_template(template_type)
    except FileNotFoundError:
        print("The template \"{}\" does not exist! The possible template names are:\n".format(template_type)+ "\t".join(available_templates()))
        sys.exit(1)

    try:
        tdoc = build(template_data, user_info)
        tdoc.write(fpath)

    # TODO: this is pretty funny
    except Exception as e:
        print(e)
        sys.exit(1)

# TODO: add error handling here
def run_update(fname, template_type, transfer=['file-specific preamble', 'main document']):
    """Update given fname to new template_type, preserving blocks in transfer"""
    # basic checks
    fpath = Path(fname)
    if not fpath.exists():
        print("Error: No file named \"{}\" to update!".format(fname))
        sys.exit(1)

    # load the document
    tdoc = TexnewDocument.load(fpath)
    #  tdoc.load(fpath)

    # generate replacement document
    template_data = load_template(template_type)
    new_tdoc = update(tdoc, template_data, transfer)

    # copy the existing file to a new location
    safe_rename(fpath)

    new_tdoc.write(fpath)

# run the test
def run_test():
    """Compile and test every template"""
    for tm in available_templates():
        tdoc = build(load_template(tm))
        errors = tdoc.verify()
        if not errors:
            print("No errors in template '{}'".format(tm))
        else:
            print("Errors in template '{}'.".format(tm))
            sys.exit(1)

