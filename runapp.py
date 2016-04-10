import os
import sublime
import sublime_plugin
import time
import subprocess

class RunappCommand(sublime_plugin.WindowCommand):
    # def __init__(self, *args):
    #     self.input = ""

    def run(self, app="", args=[], type=None, cli=False, input=False):

        target = ""
        view = None

        if self.window.active_view() != None:
            view = self.window.active_view()

            file = view.file_name()
            dir = os.path.split(file)[0]
            proj = ""

            if not input:
                # get the target string from "type"
                if type == "file":
                    target = '"'+file+'"'
                elif type == "dir":
                    target = '"'+dir+'"'
                elif type == "proj":
                    data = sublime.active_window().project_data()
                    if data != None:
                        # only use the first folder's path
                        proj = data['folders'][0]['path']
                        target = '"'+proj+'"'
                    else:
                        sublime.error_message('It\'s not a project yet. Please go to "Project->Save Project as..." firstly.')
                        return

            # handle the embedded $var$ in args
            for i in range(0,len(args)):
                arg = args[i]
                arg = arg.replace('$FILE$', '"'+file+'"')
                arg = arg.replace('$DIR$', '"'+dir+'"')
                arg = arg.replace('$PROJ$', '"'+proj+'"')
                args[i] = arg

            # handle input
            if input and view.sel() != None:
                target = view.substr(view.sel()[0])

        # invoke the application: gui or cli
        if cli == True:
            stdout, rc = self.run_cli(app, args, target)
            if rc == 0:
                output_view = self.window.create_output_panel('run-app-output')
                output_view.run_command('append', {'characters': stdout})
                self.window.run_command("show_panel", {"panel": "output.run-app-output"})
        else:
            self.run_gui(app, args, target)

    def run_gui(self, app, args, target):
        # run external gui apps, return nothing
        try:
            if sublime.platform() == 'osx':
                p = subprocess.Popen(['open', '-a', app] + args + [target], stdout=subprocess.PIPE)
            elif sublime.platform() == 'linux':
                p = subprocess.Popen([app] + args + [target], stdout=subprocess.PIPE)
            else:
                # windows uses string because of CreateProcess()
                exec_s = ' '.join(['"'+app+'"'] + args + [target])
                p = subprocess.Popen(exec_s, stdout=subprocess.PIPE)
        except:
            sublime.error_message('Error happens when run: ' + app + ', check the console')
            print("$ args: ", args)
            print("$ target: " + target)

    def run_cli(self, app, args, target, stdin=None, timeout=5, cwd=None):
        # run cli commands, return stdout, returncode
        cmd = [app] + args + [target]
        try:
          # Hide popups on Windows
          si = None
          if sublime.platform() == "windows":
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

          start = time.time()
          p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy(), startupinfo=si, cwd=cwd)
          stdout, stderr = p.communicate(input=stdin, timeout=timeout)
          p.wait(timeout=timeout)
          elapsed = round(time.time() - start)
          print("process {0} returned ({1}) in {2} seconds".format(app, str(p.returncode), str(elapsed)))
          stderr = stderr.decode("utf-8")
          if len(stderr) > 0:
            print("stderr:\n{0}".format(stderr))
          return stdout.decode("utf-8"), p.returncode

        except:
          sublime.error_message('Error happens when run: ' + app + ', check the console')
          print("$ args: ", args)
          print("$ target: " + target)

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
