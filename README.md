
# Run applications - Sublime Text

Run any customized application from command palette. Just Ctrl/Command+Shift+P, input Run XXX, that's it.

## Installation Instructions

**Package Installer**

* Install [Sublime Package Control](http://wbond.net/sublime_packages/package_control)
* Select "Package Control: Install Package" from the Command Palette (`super/ctrl+shift+p`)
* Find "Run App" and select

**Git clone**
* Enter directory through "Browse Packages..." in Sublime Text "Preferences"
* Run
    ```
    git clone https://github.com/liuhewei/run-app-sublime.git
    ```

## Usage
Preferences -> Package Settings -> Run App -> Add Application. Each application follows:
```json
    // Git bash on windows as an example, the original command is:
    // C:\\Windows\\system32\\wscript D:\\Tools\\Git\\Git Bash.vbs <directory>
    {
        "caption": "Run: Git",
        "command": "runapp",
        "args":{
          // application full path on Win/Linux, or name on MAC
          "app": "C:\\Windows\\system32\\wscript",  

          // argument list, each one is a string
          "args": ["D:\\Tools\\Git\\Git Bash.vbs"],

          // define which should follow the command:
          // "dir" - file directory 
          // "file" - file name
          // "proj" - project directory
          // "none" - nothing 
          "type": "dir"
        }
    }
```



