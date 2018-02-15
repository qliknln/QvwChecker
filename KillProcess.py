import os


class KillProcess(object):

    def __init__(self, process):
        self.process = process

    def task_kill(self):
        os.popen('TASKKILL /f /im ' + str(self.process))
