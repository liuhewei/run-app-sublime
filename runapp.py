import os
# import sys
import sublime
import sublime_plugin

class RunappCommand(sublime_plugin.WindowCommand):
    def run(self, app = "", args = [], type = ""):
        filename = self.window.active_view().file_name()
        if type == "file":
            target = filename
        elif type == "dir":
            target = os.path.split(filename)[0]
        elif type == "proj":
            data = sublime.active_window().project_data()
            if data != None:
                for folder in data['folders']:
                    target = folder['path']
                    break
            else:
                sublime.error_message('It\'s not a project yet. Please go to "Project->Save Project as..." firstly.')
                return
        elif type == "none":
            target = ""
        else:
            sublime.error_message('"type" must be one of "file", "dir", "proj", and "none".')

        if target is None:
            return

        import subprocess
        try:
            if sublime.platform() == 'osx':
                subprocess.Popen(['open', '-a', app] + args + [target])
            else:
                subprocess.Popen([app] + args + [target]) 
        except:
            sublime.error_message('Unable to open current file with "' + app + '", check the Console.')

    def is_enabled(self):
        return True

class AddappCommand(sublime_plugin.WindowCommand):
    def run(self):
        cmdFile = os.path.join(sublime.packages_path(), 'User', 'Run App.sublime-commands')
        if not os.path.isfile(cmdFile):
            # os.makedirs(cmdFile, 0o775)
            content = """[
    {
        "caption": "Run: Git",
        "command": "runapp",
        "args":{
            "app": "C:\\\\Windows\\\\system32\\\\wscript", // application name
            "args": ["D:\\\\Tools\\\\Git\\\\Git Bash.vbs"], // application arguments
            "type": "dir" // "dir", "proj", "file", "none"
        }
    }
]"""
            open(cmdFile, 'w+', encoding='utf8', newline='').write(str(content))
        sublime.active_window().open_file(cmdFile)

    def is_enabled(self):
        return True