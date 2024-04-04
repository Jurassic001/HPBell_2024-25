# HPBell_2024-25

#### Feel free to come to me or your team captains with any questions you might have

### First Time Setup:
<!-- This is intended to be a foolproof guide, so excuse the wordiness/overexplaining in some parts -->
If you already have Git, VSCode, and Python on your computer, skip to Repository Setup
1. Create a GitHub acount
2. Install [Git for windows](https://git-scm.com/download/win)
3. Install [Visual Studio Code](https://code.visualstudio.com/download)
4. Install [Python for Windows](https://www.python.org/downloads/windows/)
5. Add VSCode to your PATH variable
    <br/> 5a. Type "Enivroment Variables" into your windows search bar
    <br/> 5a. Select "Edit the system enviroment variables"
    <br/> 5a. Click the "Enivroment Variables" button (Bottom right of the new window)
    <br/> 5b. Click PATH >> Edit >> New
    <br/> 5c. Add the location of your VSCode "bin" folder
6. Run this command in the VSCode terminal <br/><br/>
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    ```

<br/><br/>

### Repository Setup:
1. Run this command to clone the repo with submodules (Needs testing):
    <br/><br/>
    ```bash
    git clone --recurse-submodules git://github.com/Jurassic001/HPBell_2024-25
    ```

<br/><br/><br/>

Template command to add git submodules (repositories inside repositories) to a repository: <br/>
```bash
git submodule add <Repository URL> <Submodule directory location>
```
<!-- 
Example command: 
git submodule add https://github.com/Jurassic001/AVR-2024 AVR\AVR-2024
^^^ This is the command I used to add the AVR-2024 repo to this repo (HPBell_2024-25) as a submodule
-->