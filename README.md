# Introduction
Script to simplify displaying information popups.

# Setup
Run setup_submodules.sh to add in required submodules.

# Outline
I can run the genpopup function (via Python or argparse) to generate notifications. I can choose to have the notifications only run when another command returns 1 and also potentially when this command returns 1 after previously returning 0.

The standard method I use is as follows:
- Set up test script that returns 1 or 0 depending upon whether I want to message to be run i.e. whether battery <10%.
- Set up script to call genpopup function when the test script returns 1.
- Call the script calling genpopup via cron.

Also, it may be sensible to implement the code to move the zenity popups to the current workspace if you use multiple workspaces. I just call this via cron regularly.
