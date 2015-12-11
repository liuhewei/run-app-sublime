import os
import sublime
import sublime_plugin

class RunappCommand(sublime_plugin.WindowCommand):
    def run(self, app = "", args = [], type = ""):
        # get the string of $FILE$
        file_s = self.window.active_view().file_name()

        # get the string of $DIR$
        dir_s = os.path.split(file_s)[0]

        # get the string of $PROJ$
        proj_s = None
        data = sublime.active_window().project_data()
        if data != None:
            for folder in data['folders']:
                proj_s = folder['path']
                break

        # handle the 'type'
        if type == "file":
            target = '"'+file_s+'"'
        elif type == "dir":
            target = '"'+dir_s+'"'
        elif type == "proj":
            if proj_s != None:
                target = '"'+proj_s+'"'
            else:
                sublime.error_message('It\'s not a project yet. Please go to "Project->Save Project as..." firstly.')
                return

        # handle the embedded $var$
        elif type == "none":
            target = ""
            for i in range(0,len(args)):
                arg = args[i]
                arg = arg.replace('$FILE$', '"'+file_s+'"')
                arg = arg.replace('$DIR$', '"'+dir_s+'"')
                if proj_s != None:
                    arg = arg.replace('$PROJ$', '"'+proj_s+'"')
                args[i] = arg

        else:
            sublime.error_message('"type" must be one of "file", "dir", "proj", and "none".')

        if target is None:
            return

        # invoke the application
        # import subprocess
        try:
            # join to one string for os.popen
            # ? subprocess.Popen can't work with msys_git 2.5.3
            exec_s = ' '.join(['"'+app+'"'] + args + [target])
            # print(exec_s)

            if sublime.platform() == 'osx':
                # subprocess.Popen(['open', '-a', app] + args + [target])
                os.popen('open -a ' + exec_s)
            else:
                # subprocess.Popen([app] + args + [target])
                os.popen(exec_s)
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
            "app": "D:\\\\Tools\\\\Git\\\\git-bash.exe",
            "args": ["--cd=$DIR$"],
            "type": "none"
        }

    },

    {
        "caption": "Run: Chrome",
        "command": "runapp",
        "args":{
            "app": "C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
            "args": [],
            "type": "file"
        }

    },
]"""
            open(cmdFile, 'w+', encoding='utf8', newline='').write(str(content))
        sublime.active_window().open_file(cmdFile)

    def is_enabled(self):
        return True