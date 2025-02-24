import os
import glob
import re
from pathspec import PathSpec

# FIX: gitignore might not be present in path; will cause erros

class Utils:
    def __init__(self) -> None:
        # TODO: make this bit into a config file
        self.taskTokens = ("TODO", "FIX", "NOTE", "ERROR")
        self.fileBuffers = list()
        self.foundTasks = list()

        self.cwd = os.getcwd()
        self.foundFiles = list()

        pass

    def pathSelector(self, chosenFolder=None) -> str:
        if chosenFolder != None: return os.path.join(self.cwd, chosenFolder)
        else: return self.cwd

    def findFiles(self, ignoreFilePath: str):
        
        if not os.path.isfile(ignoreFilePath):
            raise Exception(f"No such file named {ignoreFilePath} in: {self.cwd}")

        with open(ignoreFilePath, 'r', encoding='utf-8') as f:
            ignFile = f.readlines()

            spec = PathSpec.from_lines('gitwildmatch', ignFile)

            fmtGlobPath = os.path.join(self.pathSelector(), "**")

            for name in glob.glob(fmtGlobPath, recursive=True):
                matchedRef = re.search(r'^.+\.[a-zA-Z0-9]+$', name)

                if matchedRef: 
                    if not spec.match_file(name): self.foundFiles.append(name)

            return self.foundFiles

    def fetchBuffer(self) -> list[dict]:
        for file in self.foundFiles:
            if os.path.isfile(file):
                with open(file,'r') as fopen_buffer:
                    newBuffer = {"filename": file, "buffer": fopen_buffer.readlines()}
                    self.fileBuffers.append(newBuffer)

        return self.fileBuffers

    def fetchTasks(self):
        for iDicts in self.fileBuffers: 

            for line in iDicts["buffer"]: 
                fmtLine = line.replace('\n', '').replace('    ', '')

                if fmtLine.startswith('#') & any(temp in fmtLine for temp in self.taskTokens): 
                    self.foundTasks.append(fmtLine)

            if len(self.foundTasks) > 0: 
                relativePath = os.path.relpath(iDicts["filename"], self.cwd)
                taskAmount = len(self.foundTasks)

                print(f"\x1b[1;90m\n@ {relativePath} :: found {taskAmount} tasks!\x1b[0m\n")

                for i in self.foundTasks: 
                    print(f"\t\x1b[1;96m{i}\x1b[0m")

                self.foundTasks.clear()
        pass
