
# Run applications - Sublime Text

Run any customized application from command palette. Just Ctrl/Command+Shift+P, input `Run: XXX`, that's it!

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
Firstly, add applications through: "Preferences" -> "Package Settings" -> "Run App" -> "Add Application". 

Each application follows:
```
    {
        "caption": "Run: Git",  // cannot be changed
        "command": "runapp",    // cannot be changed
        "args":{
          // application full path on Win/Linux, or only name on MAC
          "app": "",  

          // argument list
          "args": [""], 

          // define which should follow the command:
          // "dir" - file directory 
          // "file" - file name
          // "proj" - project directory
          // "none" - nothing 
          "type": ""  
        }
    }
```

Take "Git bash on windows" as an example, the original command is:
`C:/Windows/system32/wscript D:/Tools/Git/Git Bash.vbs <directory>`

```json
    {
        "caption": "Run: Git",
        "command": "runapp",
        "args":{
          "app": "C:\\Windows\\system32\\wscript",  
          "args": ["D:\\Tools\\Git\\Git Bash.vbs"], 
          "type": "proj"
        }
    }
```



