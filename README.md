# HPBell_2024-25

This repository contains code for the AVR and Dexi drones, as well as the ground RVR vehicle, for the 2024 Bell AVR competition season.
<!-- Our team name is Zephyrus, the greek god of western winds -->
#### Feel free to come to Max or your team captains with any questions/issues you might have

## To do
<!--
Surround content with double tilde to cross out
i.e. ~~<list item>~~
-->
- ~~Setup team repo with submodules~~
- ~~Add a "How to Use" section~~
- Create Dexi drone movement framework
- Add more things to the to do list

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
1. Press CTRL + Shift + P
2. Type `git pull`
    - If it prompts you to choose a repository, select `HPBell_2024-25`

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

<!--
<br/> The next thing:
```
placeholder
```
-->