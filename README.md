# HPBell_2024-25

#### Feel free to come to me or your team captains with any questions/issues you might have

## To do
- [x] Setup team repo with submodules
- [ ] Create Dexi drone movement framework
- [ ] Add more things to the to do list

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
    git clone --recurse-submodules git://github.com/Jurassic001/HPBell_2024-25 ~/Documents/VSCode/HPBell_2024-25
    code Documents/VSCode/HPBell_2024-25
    ```
3. Once in VSCode, open and run `installReqs.py` to install required Python packages
4. And you're ready to start contributing!
    - If you intend to work on the AVR code, your setup process is far from over.
<!--
Do this on the VMC maybe:
git clone --recurse-submodules https://github.com/bellflight/AVR-2022 ~/AVR-2022
-->

<br/>

## Misc:
Template command to add git submodules (repositories inside repositories) to a repository:
```bash
git submodule add <Repository URL> <Submodule directory from root>
```
<!--
Example command:
git submodule add https://github.com/Jurassic001/AVR-2024 AVR\AVR-2024
^^^ This is the command I used to add the AVR-2024 repo to this repo (HPBell_2024-25) as a submodule
-->

<br/> Creating/updating requirements.txt:
```bash
pipreqs --force --ignore AVR/AVR-2024
# Ignores the AVR submodule which has its own requirements.txt files
```
<!--
<br/> The next thing:
```
placeholder
```
-->