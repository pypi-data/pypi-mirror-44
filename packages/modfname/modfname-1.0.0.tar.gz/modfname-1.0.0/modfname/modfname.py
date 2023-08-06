import sys
import os
import getpass

from os import stat
from pwd import getpwuid

import logging
# from .logger import build_logger
from logger import build_logger
logger = build_logger("modfname", level=logging.INFO)


# important constants:

# colors
CRED = '\033[31m'
CBYELLOW = '\033[1;33m'
CBWHITE = '\033[1;37m'
CBPURPLE = '\033[1;35m'
# BBLACK = '\033[1;30m'
CLIGHTBLUE = '\033[94m'
CBBLUE = '\033[1;34m'
CNORMAL_WHITE = '\033[0m'

COCCURRENCES = CBPURPLE
CFILE_PATHS = CBBLUE
CTEXT_FILES = CBWHITE

# indicator strings
INIT_STRINGS = ["--initial", "--init"]
DESTINATION_STRINGS = ["--destination", "--dest"]
RECURSIVE_STRINGS = ["--recursive", "--rec"]
PATHS_STRINGS = ["--paths"]
END_FLAG_STRINGS = ["--end_param", "--end"]

# supported short indicators
SUPPORTED_SHORT_INDICATORS = ['i', 'd', 'r', 'p']


def check_help_request(arguments):
    if len(arguments) == 1 and (arguments[0] == "-h" or arguments[0] == "--help"):
        README_path = "/usr/lib/modfname/README.md"

        f = open(README_path, 'r')
        print(CFILE_PATHS + "\n\t#######      modfname documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '')
            line = line.replace('```', '')
            line = line.replace('<pre>', '')
            line = line.replace('</b>', '')
            line = line.replace('<b>', '')
            line = line.replace('<!-- -->', '')
            line = line.replace('<br/>', '')
            line = line.replace('```sh', '')
            line = line.replace('***', '')
            line = line.replace('**', '')
            line = line.replace('*', '')
            print(" " + line, end='')
        print(CNORMAL_WHITE)
        exit()


def check_nb_parameters(args):
    if len(args) < 3:
        logger.error("no enough arguments")
        raise ValueError("no enough arguments. Needs at least the initial string, the destination string and "
                         "one file/folder path such as:\nmodfname -r \" \" \"_\" \"$MHOME/dev/tests/this is a test\"")


def initiate_values():
    recursive = False
    init_strs = []
    dest_str = None
    filepaths = []
    nb_occs = [0, 0]  # 0: found, 1: replaced
    return recursive, init_strs, dest_str, filepaths, nb_occs


def treat_input_parameters(input_args, recursive, init_strs, dest_str, filepaths):

    nb_args = len(input_args)
    args_not_used_indexes = list(range(nb_args))
    for arg_index, arg in enumerate(input_args):
        if arg.startswith("--"):
            if arg in INIT_STRINGS + DESTINATION_STRINGS + RECURSIVE_STRINGS + PATHS_STRINGS + END_FLAG_STRINGS:
                if arg in RECURSIVE_STRINGS:
                    recursive = True
                elif arg in END_FLAG_STRINGS:
                    pass

                elif arg_index < nb_args - 1:
                    if arg in INIT_STRINGS:
                        get_arg_list(input_args, arg_index, args_not_used_indexes, init_strs)

                    if arg in DESTINATION_STRINGS:
                        dest_str = input_args[arg_index + 1]
                        args_not_used_indexes.remove(arg_index + 1)

                    if arg in PATHS_STRINGS:
                        get_arg_list(input_args, arg_index, args_not_used_indexes, filepaths)

                else:
                    logger.error("no parameter after %s indicator" % arg)
                    raise ValueError("needs a parameter after the %s indicator" % arg)

                args_not_used_indexes.remove(arg_index)

            else:
                logger.error("the indicator %s is not supported" % arg)
                raise ValueError("please remove the %s parameter from the command" % arg)
        elif arg.startswith("-"):
            for short_ind in arg[1:]:
                if short_ind not in SUPPORTED_SHORT_INDICATORS:
                    logger.error("the short indicator -%s is not supported" % short_ind)
                    raise ValueError("please remove the -%s short indicator from the command" % short_ind)
                elif short_ind == 'i':
                    get_arg_list(input_args, arg_index, args_not_used_indexes, init_strs)
                elif short_ind == 'd':
                    dest_str = input_args[arg_index + 1]
                    args_not_used_indexes.remove(arg_index + 1)
                elif short_ind == 'r':
                    recursive = True
                elif short_ind == 'p':
                    get_arg_list(input_args, arg_index, args_not_used_indexes, filepaths)

            args_not_used_indexes.remove(arg_index)
    return recursive, dest_str, args_not_used_indexes


def get_arg_list(input_args, ref_arg_index, args_not_used_indexes, input_list):
    for arg_index, arg in enumerate(input_args[ref_arg_index + 1:]):
        if not arg.startswith("-"):
            input_list.append(arg)
            args_not_used_indexes.remove(ref_arg_index + 1 + arg_index)
        else:
            return input_list


def get_final_params(input_args, args_not_used_indexes, init_strs, dest_str, filepaths):

    if not filepaths:
        if not args_not_used_indexes:
            logger.error("arguments are missing ... please review the command syntax.")
            raise ValueError("the file path arg is not defined")
        for arg_not_used_index in args_not_used_indexes:
            filepaths.append(input_args[arg_not_used_index])
            args_not_used_indexes.pop()
    elif not dest_str:
        if not args_not_used_indexes:
            logger.error("arguments are missing ... please review the command syntax.")
            raise ValueError("the destination string arg is not defined")
        dest_str = input_args[-1]
        args_not_used_indexes.pop()
    elif not init_strs:
        if not args_not_used_indexes:
            logger.error("arguments are missing ... please review the command syntax.")
            raise ValueError("the initial strings arg is not defined")
        for arg_not_used_index in args_not_used_indexes:
            init_strs.append(input_args[arg_not_used_index])
            args_not_used_indexes.pop()

    if args_not_used_indexes:
        logger.error("too much arguments entered ... please review the command syntax.")
        raise ValueError("the args %s have not been used" % args_not_used_indexes)

    return dest_str


def print_WARNING_in_red():
    print(CRED + "\n\tWARNING:" + CNORMAL_WHITE, end='')


def check_user_permissions(file_path):
    current_user = getpass.getuser()
    owner_file = getpwuid(stat(file_path).st_uid).pw_name
    if owner_file != current_user:
        print_WARNING_in_red()
        print(" the file " + CFILE_PATHS + "%s" % file_path + CNORMAL_WHITE + " is owned by " + CFILE_PATHS +
              "%s" % owner_file + CNORMAL_WHITE + ", might be necessary to manage its permissions\n")


def concatenate_paths(root_path, final_path):
    if root_path.endswith('/') and final_path.startswith('/'):
        global_path = root_path[:-1] + final_path
    elif (root_path.endswith('/') and not final_path.startswith('/')) or (not root_path.endswith('/') and final_path.startswith('/')):
        global_path = root_path + final_path
    else:
        global_path = root_path + '/' + final_path
    return global_path


def check_folder_path_exists(folderpath):
    if not os.path.isdir(folderpath):
        print_WARNING_in_red()
        print(CFILE_PATHS + " %s " % folderpath + CNORMAL_WHITE + "folder doesn't exist")
        raise ValueError("the directory path to apply %s doesn't exist, you may review it" % folderpath)


def check_path_exists(path):
    if not os.path.exists(path):
        print_WARNING_in_red()
        print(CFILE_PATHS + " %s " % path + CNORMAL_WHITE + "path doesn't exist")
        return False
    return True


def abort_process():
    print(CBYELLOW + "\n\n\t\t\taborted ...\n\t\t\t\tSee you later\n" + CNORMAL_WHITE)
    exit()


def init_strs_to_dest_str(init_path, init_strs, dest_str, nb_occs):
    base_path = os.path.dirname(init_path)
    fname = os.path.basename(init_path)
    fname_origin = fname

    for init_str in init_strs:
        if init_str in fname:
            nb_occs[0] += 1
            fpath = concatenate_paths(base_path, fname)
            print("\nthere is " + COCCURRENCES + "\"%s\"" % init_str + CNORMAL_WHITE + " in " + CFILE_PATHS + "%s" % fpath + CBWHITE)

            new_fname = fname.replace(init_str, dest_str)
            mod_fname_check = input("\tchange " + COCCURRENCES + "%s" % fname + CBWHITE + " to " + COCCURRENCES + "%s" % new_fname + CBWHITE +
                                    " ?\n\t[ENTER] to proceed\t[sS] to skip\t[aA] to abort process\n")

            if mod_fname_check == "":
                fname = new_fname
                nb_occs[1] += 1
            elif mod_fname_check in ["a", "A"]:
                abort_process()
            else:
                print(CFILE_PATHS + "\n%s" % fpath + CBWHITE + " not changed")

    if fname != fname_origin:
        new_path = concatenate_paths(base_path, fname)
        os.rename(init_path, new_path)
        print(CFILE_PATHS + "\t%s/" % os.path.dirname(new_path) + COCCURRENCES + "%s" % os.path.basename(init_path) + CFILE_PATHS + "\tdone\n")
        return new_path

    return init_path


def mod_fnames(fpath, init_strs, dest_str, recursive, nb_occs):

    check_user_permissions(fpath)

    if os.path.isfile(fpath):
        init_strs_to_dest_str(fpath, init_strs, dest_str, nb_occs)

    if os.path.isdir(fpath):
        fpath = init_strs_to_dest_str(fpath, init_strs, dest_str, nb_occs)
        if recursive:
            list_files_and_folders = os.listdir(fpath)
            for file_or_folder_name in list_files_and_folders:
                mod_fnames(concatenate_paths(fpath, file_or_folder_name), init_strs, dest_str, recursive, nb_occs)


def occs_summary(nb_occs, init_strs):
    if nb_occs[0] == 0:
        print(CFILE_PATHS + "\n\t0" + CNORMAL_WHITE + " occurrence of " + COCCURRENCES + "%s" % init_strs + CNORMAL_WHITE + " found")
    elif nb_occs[0] == 1:
        print(CFILE_PATHS + "\n\t1" + CNORMAL_WHITE + " occurrence of " + COCCURRENCES + "%s" % init_strs +
              CNORMAL_WHITE + " found and " + CFILE_PATHS + "%s" % nb_occs[1] + CNORMAL_WHITE + " replaced")
    else:
        print(CFILE_PATHS + "\n\t%s" % nb_occs[0] + CNORMAL_WHITE + " occurrences of " + COCCURRENCES + "%s" % init_strs
              + CNORMAL_WHITE + " found and " + CFILE_PATHS + "%s" % nb_occs[1] + CNORMAL_WHITE + " replaced")


def main():

    input_args = sys.argv[1:]
    check_help_request(input_args)
    check_nb_parameters(input_args)
    recursive, init_strs, dest_str, filepaths, nb_occs = initiate_values()

    recursive, dest_str, args_not_used_indexes = treat_input_parameters(input_args, recursive, init_strs, dest_str, filepaths)

    dest_str = get_final_params(input_args, args_not_used_indexes, init_strs, dest_str, filepaths)

    if recursive:
        if len(filepaths) != 1:
            logger.error("in recursive mode only one folder path must be given\ngiven %s" % filepaths)
            raise ValueError("please enter only one input folder path in recursive mode")

        folder_path = filepaths[0]
        check_folder_path_exists(folder_path)
        if not folder_path.startswith('/'):
            folder_path = concatenate_paths(os.getcwd(), folder_path)

        files_folders = os.listdir(folder_path)
        for file_or_folder_name in files_folders:
            mod_fnames(concatenate_paths(folder_path, file_or_folder_name), init_strs, dest_str, recursive, nb_occs)
    else:
        if len(filepaths) == 0:
            logger.error("needs at least one file/folder path")
            raise ValueError("please enter at least one path")

        for filepath in filepaths:
            if not filepath.startswith('/'):
                filepath = concatenate_paths(os.getcwd(), filepath)
            if not check_path_exists(filepath):
                print(CFILE_PATHS + "\n\t\t\tskipped\n\n" + CNORMAL_WHITE)
                continue
            mod_fnames(filepath, init_strs, dest_str, recursive, nb_occs)

    occs_summary(nb_occs, init_strs)


if __name__ == "__main__":
    main()
