# Introduction
Script to simplify displaying information popups.

# Installation
This requires zenity and python to be installed.

<!---INSTALLATION_STANDARD_START.-->
I found standard methods for managing submodules to be a little complicated so I use my own method for managing my submodules. I use the mysubmodules project to quickly install these. To install the project, it's therefore sensible to download the mysubmodules project and then use a script in the mysubmodules project to install the submodules for this project.

If you are in the directory where you wish to download linux-popupinfo i.e. if you wish to install the project at /home/files/linux-popupinfo/ and you are at /home/files/, and you have not already cloned the directory to /home/files/linux-popupinfo/, you can run the following commands to download the directory:

```
git clone https://github.com/c-d-cotton/mysubmodules.git getmysubmodules
python3 getmysubmodules/singlegitmodule.py linux-popupinfo --downloadmodule --deletegetsubmodules
```

The option --downloadmodule downloads the actual module before installing the submodules. The option --deletegetsubmodules deletes the getsubmodules project after the submodules are installed.

If you have already downloaded projectdir to the folder /home/files/linux-popupinfo/, you can add the submodules by running the following commands from the directory /home/files/:
```
git clone https://github.com/c-d-cotton/mysubmodules.git getmysubmodules
python3 getmysubmodules/singlegitmodule.py linux-popupinfo --deletegetsubmodules
```
<!---INSTALLATION_STANDARD_END.-->


# Outline
I can run the genpopup function (via Python or argparse) to generate notifications. I can choose to have the notifications only run when another command returns 1 and also potentially when this command returns 1 after previously returning 0.

The standard method I use is as follows:
- Set up test script that returns 1 or 0 depending upon whether I want to message to be run i.e. whether battery <10%.
- Set up script to call genpopup function when the test script returns 1.
- Call the script calling genpopup via cron.

Also, it may be sensible to implement the code to move the zenity popups to the current workspace if you use multiple workspaces. I just call this via cron regularly.
