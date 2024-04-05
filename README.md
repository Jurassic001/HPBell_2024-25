# HPBell_2024-25

#### Feel free to come to me or your team captains with any questions/issues you might have

### First Time Setup:
<!-- This is intended to be a foolproof guide, so excuse the wordiness/overexplaining in some parts -->
<!--
###### If you already have Git, VSCode, and Python on your computer, skip to [Repository Setup](https://github.com/Jurassic001/HPBell_2024-25?tab=readme-ov-file#repository-setup)
-->
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

    ```cmd
    git clone --recurse-submodules git://github.com/Jurassic001/HPBell_2024-25 ~/Documents/VSCode/HPBell_2024-25
    code Documents/VSCode/HPBell_2024-25
    ```
<!--
Do this on the VMC maybe:
git clone --recurse-submodules https://github.com/bellflight/AVR-2022 ~/AVR-2022
-->

<br/>

### Misc:
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
pipreqs --force
# It's likely that you'll have to venture deep into the VMC folder to get this command to run without error
```
<!--
<br/> The next thing:
```bash
placeholder
```
-->