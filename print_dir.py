#!/usr/bin/env python3

import os, sys
from stat import *


global print_layer_ctrl
print_layer_ctrl = 0

PRINT_FILE   = 1
PRINT_SCREEN = 2

global file_handler, print_mode

print_mode = PRINT_SCREEN

file_handler = None

def walktree(top):

    global print_layer_ctrl

    print_layer_ctrl += 1

    try:
        fl = os.listdir(top)
        
    except:
        
        print_layer_ctrl -= 1
        my_print("Wrong Folder Name: %s" % top)
        return
            
    for f in os.listdir(top):

        try:
            pathname = os.path.join(top, f)
            fl_att = os.stat(pathname) 
        except:
            continue
        
        if S_ISDIR(fl_att.st_mode):
            # It's a directory, recurse into it

            if len(f)>0 and f[0] != '.':

                fmt = "%" + str(print_layer_ctrl*2+2+len(f)+2) + "s"

                my_print(fmt % ("└─[" + f + "]",))

                walktree(pathname)

                print_layer_ctrl -= 1

            else:
                pass

        elif S_ISREG(fl_att.st_mode):
            # It's a file, print it
            fmt = "%" + str(print_layer_ctrl*2 + 2 + len(f)) + "s"
            my_print(fmt % ("└─" + f,))

        else:
            # Unknown file type, print a message
            my_print('Skipping %s' % pathname)


def validate_folder_name(s):

    s_org = s
    
    if len(s) > 1 and s[-1] != '\\':
        s = s + '\\'

    try:
        os.listdir(s) 
    except:
        print("Wrong Folder Name: %s" % s_org)
        return
    
    my_print("[" + s_org + ']')

    walktree(s)


def my_print(s):

    if print_mode == PRINT_SCREEN:
        print(s)
    else:
        try:
            file_handler.write(s + "\n")
            print(s)
            
        except:
            print("Failed to write to file")
                      


def main():

    global file_handler, print_mode
    
    if len(sys.argv) > 1:
        s = sys.argv[1]
        
        if s == '?':
            print("python print_dir [dir] [-file_name to save result]")
            return          
    else:
        s= input("Please input the director to be displayed:")
    
    if len(sys.argv) > 2:

        filename = sys.argv[2]

        try:
            file_handler = open(filename, 'w+')
        except:
            print("Wrong file name to be opened " + filename)
            return

        print_mode = PRINT_FILE

    else:
        print_mode = PRINT_SCREEN
       
    validate_folder_name(s)  #  start to walk through the directory

    if print_mode == PRINT_FILE:
        file_handler.close()
        print("\nDirectory Structure Has been Written to " + filename + ".")


if __name__ == '__main__':
    main()
