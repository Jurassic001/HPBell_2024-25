# HPBell_2024-25

This repository contains code for the AVR and Dexi drones, as well as the ground RVR vehicle, for the 2024 Bell AVR competition season.
<!-- Our team name is Zephyrus, the greek god of western winds -->
#### Feel free to come to Max or your team captains with any questions/issues you might have

## Setup
### First Timer Setup:
<!-- This is intended to be a foolproof guide, so excuse the wordiness/overexplaining in some parts -->
1. Create a GitHub acount
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Install [Visual Studio Code](https://code.visualstudio.com/download)
    - IMPORTANT: When installing make sure to check the "Add to PATH" box.
4. Install [Python for Windows](https://www.python.org/downloads/windows/)
    - IMPORTANT: During installation check the "Install pip" & "Add Python to enviroment variables" boxes. Leave all other options as default.
    
    <br/>

### Repository Setup:
1. Open the command prompt
2. Run this command to download this repo and open it (Will take 5-10 minutes):

    ```
    git clone --recurse-submodules https://github.com/Jurassic001/HPBell_2024-25 Documents/VSCode/HPBell_2024-25
    code Documents/VSCode/HPBell_2024-25
    ```
3. Once in VSCode, you're ready to start contributing!
    - If you intend to work on the AVR code, your setup process isn't over. Run `code Documents/VSCode/HPBell_2024-25/AVR/AVR-2024` in the command prompt and take a look at the README to see what you need to do.
<!--
Do this on the VMC maybe:
git clone --recurse-submodules https://github.com/bellflight/AVR-2022 ~/AVR-2022
-->

<br/>

## How to use

### Making changes:
1. Go to the Source Control tab on the left
2. Stage your changes (Click the plus on all files that you worked on)
3. Write a short sentence about the changes you made
4. Press commit
5. Press sync

### Getting changes:
1. Press <kbd>CTRL</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
2. Type `git pull`
    - If it prompts you to choose a repository, select `HPBell_2024-25`

<br/>

## Connecting to drones
First, install [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). We'll use Putty to connect to the Jetson Nano (commonly referred to as the VMC) on the AVR drone and the ARK Pi6X Flow on the DEXI.

### Connecting to the Jetson on the AVR
1. Connect to the `Varsity Bells` wifi network
    - Password is `May152006!`
2. Open the run dialogue on Windows or your terminal on any other machine
    - The run dialogue (<kbd>Windows</kbd> + <kbd>R</kbd>) keeps a history of previous commands, so if you value efficiency and automation I highly recommend using it
3. Run `putty.exe -ssh avr@drone -pw bellavr22`
4. You are in the command line of the Jetson now. If you don't know what commands to run, google it (i.e. "How to move around in Linux command line) or look at some of the other README's in AVR-2024

### Connecting to the ARK on the DEXI
1. Connect to the `dexi_002d` wifi network
    - Password is `droneblocks`
2. Open the run dialogue on Windows or your terminal on any other machine
3. Run `putty.exe -ssh dexi@192.168.4.1 -pw dexi`
4. You are connected!

<br/>

## Misc
Template command to add git submodules (repositories inside repositories) to a repository:
```bash
git submodule add <Repository URL> <Submodule directory from root>
```
<!--
Example command:
git submodule add https://github.com/Jurassic001/AVR-2024 AVR\AVR-2024
^^^ This is the command I used to add the AVR-2024 repo to this repo (HPBell_2024-25) as a submodule
-->

<br/>

Command to remove remote branches from VSCode that've already been deleted on Github:
```bash
git fetch --prune
```

<!--
<br/>

The next thing:
```
placeholder
```
-->