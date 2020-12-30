#!/usr/bin/env python
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

# OLD:{{{1
def genpopup(text, textiscommand = False, title = None, testcommand = None, testcommandonlynewfile = None, appendpid = True):
    """
    text is normally text to print.
    textiscommand = True means text is actually command to run and print the output of that command in message.

    title is the title of the Zenity textbox

    testcommand is a command that returns 1 or 0. Popup only executes when returns 1.
    testcommandonlynewfile is a filename. Write last testcommand return to that file. Then require testcommand = 1 and previous testcommand = 0 for the command to execute.

    appendpid appends the pid to a textfile in case I want to move them to the current workspace using the movezenitycurrentworkspace function.
    """
    import subprocess

    # decide whether to run popup
    runpopup = False
    if testcommand is None:
        runpopup = True
    else:
        testcommandoutput = subprocess.check_output(testcommand, shell = True)
        testcommandoutput = testcommandoutput.decode('latin-1').strip()
        if testcommandoutput not in ['0', '1']:
            raise ValueError('testcommandoutput does not return "0" or "1"')
        else:
            testcommandoutput = int(testcommandoutput)
            
        if testcommandonlynewfile is None:
            if testcommandoutput == 1:
                runpopup = True
        else:
            if os.path.isfile(testcommandonlynewfile):
                with open(testcommandonlynewfile, 'r') as f:
                    lasttestcommandoutput = f.read().strip()
                if lasttestcommandoutput not in ['0', '1']:
                    raise ValueError('lasttestcommandoutput does not return "0" or "1"')
                lasttestcommandoutput = int(lasttestcommandoutput)
            else:
                # if file does not exist, say command failed last time
                lasttestcommandoutput = 0

            # run command
            if lasttestcommandoutput == 0 and testcommandoutput == 1:
                runpopup = True

            # save testcommandoutput to testcommandonlynewfile
            with open(testcommandonlynewfile, 'w+') as f:
                f.write(str(testcommandoutput))

    if runpopup is True: 
        if textiscommand is True:
            commandoutput = subprocess.check_output(text, shell = True)
            commandoutput = commandoutput.decode('latin-1')
        else:
            commandoutput = text

        # replace quotation marks so don't get confused when pass to bash
        zenityargs = ["zenity", "--info", "--display=:0.0", "--text", commandoutput.replace("\"", "\\\"")]
        # the display argument is needed to work with cron: see http://promberger.info/linux/2009/01/02/running-x-apps-like-zenity-from-crontab-solving-cannot-open-display-problem/

        if title is not None:
            zenityargs = zenityargs + ["--title", title]

        # note use Popen so opens in background
        p = subprocess.Popen(zenityargs)

        if appendpid is True:
            if not os.path.isdir('/tmp/linux-popupinfo/'):
                os.mkdir('/tmp/linux-popupinfo/')

            with open('/tmp/linux-popupinfo/popups.txt', 'a+') as f:
                f.write(str(p.pid) + '\n')

        return(p.pid)

# genpopup(text = 'echo hello', textiscommand = True, testcommand = 'echo 1', title = '1234')

def genpopup_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--textiscommand", action = 'store_true')
    parser.add_argument("--title")
    parser.add_argument("--testcommand")
    parser.add_argument("--testcommandonlynewfile")
    parser.add_argument("--appendpid", action = 'store_false')
    
    args=parser.parse_args()
    #End argparse:}}}
    
    pid = genpopup(args.text, textiscommand = args.textiscommand, title = args.title, testcommand = args.testcommand)

# Generate popups:{{{1
def genpopup_basic(message, title = None, appendpid = True):
    import subprocess

    # replace quotation marks so don't get confused when pass to bash
    zenityargs = ["zenity", "--info", "--display=:0.0", "--text", message.replace("\"", "\\\"")]
    # the display argument is needed to work with cron: see http://promberger.info/linux/2009/01/02/running-x-apps-like-zenity-from-crontab-solving-cannot-open-display-problem/

    if title is not None:
        zenityargs = zenityargs + ["--title", title]

    # note use Popen so opens in background
    p = subprocess.Popen(zenityargs)

    if appendpid is True:
        if not os.path.isdir('/tmp/linux-popupinfo/'):
            os.mkdir('/tmp/linux-popupinfo/')

        with open('/tmp/linux-popupinfo/popups.txt', 'a+') as f:
            f.write(str(p.pid) + '\n')

# genpopup_basic('echo hello', title = '1234')


def genpopup_test(message, title = None, test = None, combined = False, pythoninput = False, pythoninput_message = False, pythoninput_test = False, shellinput = False, shellinput_message = False, shellinput_test = False, testnewlytrue = False, combinedsep = '', appendpid = True, savefile = None, savefolder = None):
    """
    message is the text used in the popup or the command used to generate a message.
    test is a command used to test whether or not the command should be run.
    If combined is True then the message and test are actually given in the message argument (or by running it) where the first character is the test (0/1) and the rest is the message.

    The input for message can be given as text, a shell input i.e. running a shell command or a Python function. Default: text.
    The input for message can be given as True/False, a shell input or a Python function. Default: True/False (or 0/1).
    This is what the input commands are about.

    If testnewlytrue is True then return True for the test only if the last time the command was run it was False or it has not been run before.

    intervals allow me to generate the popup if it is x seconds after the command was last run where the test was False where x is an integer in the list of intervals. This doesn't make sense to use with testnewlytrue.

    should have combined is True or test is not None otherwise no point in using this function and should just use basic function
    """
    import subprocess

    if combined is False and test is None:
        ValueError('combined is False and test is None. This doesn\'t make sense when I am running a function to test before running the message.')

    if savefolder is not None and savefile is None:
        savefile = savefolder + 'info.txt'

    if shellinput is True:
        shellinput_message = True
        shellinput_test = True

    if pythoninput is True:
        pythoninput_message = True
        pythoninput_test = True

    # get message
    # this isn't completely efficient since might not use message if combined is False and test fails but...
    if shellinput_message is True:
        messageoutput = subprocess.check_output(message, shell = True)
        messageoutput = messageoutput.decode('latin-1')
    elif pythoninput_message is True:
        messageoutput = message()
    else:
        messageoutput = message

    # remove combined
    if combined is True:
        testoutput = message[0]
        messageoutput = message[1]

    # get test if appropriate
    if test is not None:
        if shellinput_test is True:
            testoutput = subprocess.check_output(test, shell = True)
            testoutput = testoutput.decode('latin-1')
        elif pythoninput_test is True:
            testoutput = test()
        elif test is True:
            testoutput = 1
        elif test is False:
            testoutput = 0
        else:
            testoutput = test

        # check testoutput is 0,1 and convert to integer
        try:
            testoutput = int(testoutput)
        except Exception:
            ValueError('testoutput is not 0 or 1')

    # checking whether the last test was False if appropriate
    if testnewlytrue is True:
        if os.path.isfile(savefile):
            with open(savefile, 'r') as f:
                lasttestoutput = f.read().strip()
            if lasttestoutput not in ['0', '1']:
                raise ValueError('lasttestcommandoutput does not return "0" or "1"')
            lasttestoutput = int(lasttestoutput)
        else:
            # if file does not exist, say command failed last time
            lasttestoutput = 0

        # save testcommandoutput to testcommandonlynewfile
        with open(savefile, 'w+') as f:
            f.write(str(testoutput))
        
        # adjust whether run command
        # need to do this after save current testoutput
        if lasttestoutput == 1:
            testoutput = 0

    if testoutput == 1:
        testoutputboolean = True
    else:
        testoutputboolean = False

    if testoutputboolean is True:
        genpopup_basic(message, title = title, appendpid = appendpid)


# Move popups to current screen:{{{1
def check_pid(pid):        
    """
    Check For the existence of a unix pid.
    Taken from http://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid
    """
    import os

    try:
        os.kill(pid, 0)
    except Exception:
        return False
    else:
        return True



def movezenitycurrentworkspace():
    """
    Move zenity popups created by genpopup to the current workspace.
    This is necessary since otherwise the popups will just appear on the workspace on which the script generating the popups was run.
    """
    import subprocess

    if not os.path.isfile('/tmp/linux-popupinfo/popups.txt'):
        return(None)

    with open('/tmp/linux-popupinfo/popups.txt', encoding = 'latin-1') as f:
        pidlist = [int(pid) for pid in f.read().splitlines()]

    sys.path.append(str(__projectdir__ / Path('submodules/linux-winfunc/')))
    from winfunc import getcurdesktop
    currentworkspace = getcurdesktop()

    newpidlist = []
    for pid in pidlist:
        if check_pid(pid) is True:
            newpidlist.append(pid)

    with open('/tmp/linux-popupinfo/popups.txt', 'w+') as f:
        f.write('\n'.join([str(pid) for pid in newpidlist]))
    
    if len(newpidlist) > 0:
        pid = newpidlist[0]

        sys.path.append(str(__projectdir__ / Path('submodules/linux-winfunc/')))
        from winfunc import visualpidfrompid
        visualpid = visualpidfrompid(pid)

        output = subprocess.check_output(['wmctrl', '-l'])
        output = output.decode('latin-1').splitlines()
        for line in output:
            linesplit = line.split()
            if linesplit[0] == visualpid:
                workspace = linesplit[1]

        sys.path.append(str(__projectdir__ / Path('submodules/linux-winfunc/')))
        from winfunc import changedesktop
        changedesktop(workspace)
                

            



def movezenitycurrentworkspace_while():
    """
    My own daemon to keep running indefinitely.
    Obiously, need to put process to background when start.
    """
    import time
    while True:
        movezenitycurrentworkspace()

        time.sleep(10)
