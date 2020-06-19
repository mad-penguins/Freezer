from os import getcwd
from sys import argv
import configparser
import os
from os import mkdir, walk, path
import re
import importlib.util
import shutil
from time import sleep

class Freezer(object):
    """docstring for Freezer"""
    def __init__(self, args, workingDirectory):
        super(Freezer, self).__init__()
        self.args = args
        self.workingDirectory = workingDirectory

    def getListFromConfig(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.args[1])

        a = config.get(section, key)
        a = a.strip('][').split(', ')
        for x in range(len(a)):
            a[x] = a[x].strip("'")

        if (len(a) == 1) and (a[0] == ''):
            a = list()
        return a

    def configHasSection(self, section):
        config = configparser.ConfigParser()
        config.read(self.args[1])

        if config.has_section(section):
            return True
        return False

    def configHasOption(self, section, option):
        config = configparser.ConfigParser()
        config.read(self.args[1])

        if config.has_option(section, option):
            return True
        return False

    def writeConfig(self, section, option, value, nameConfig=None):
        if nameConfig is None:
            nameConfig = self.args[1]

        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(nameConfig)

        if not config.has_section(section):
            config.add_section(section)
        config[section][option] = str(value)

        with open(nameConfig, "w") as config_file:
            config.write(config_file)

    def readConfig(self, section, option, nameConfig=None):
        if nameConfig is None:
            nameConfig = self.args[1]

        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(nameConfig)

        if not config.has_option(section, option):
            return None
        return config[section][option]


    def startNewProject(self, nameNewProject = None):
        if nameNewProject is None:
            nameNewProject = self.args[2]

        self.writeConfig("Project", "Name", nameNewProject, nameNewProject+'.freezer')
        self.writeConfig("Build", "DIR", "build", nameNewProject+'.freezer')
        self.writeConfig("Source", "DIR", "src", nameNewProject+'.freezer')
        self.writeConfig("Static", "DIR", "static", nameNewProject+'.freezer')
        self.writeConfig("Snowflakes *.html", "DIR", "snow", nameNewProject+'.freezer')
        self.writeConfig("Snowflakes *.py", "DIR", "py", nameNewProject+'.freezer')
        self.writeConfig("Snowflakes *.*", "DIR", "var", nameNewProject+'.freezer')
        self.writeConfig("Snowflakes *.cfreezer", "DIR", "conf", nameNewProject+'.freezer')
        self.writeConfig("Snowflakes *.cfreezer", "path", str(list()), nameNewProject+'.freezer')

        mkdir("src")
        mkdir("snow")
        mkdir("py")
        mkdir("var")
        mkdir("conf")
        mkdir("static")

    def getFileAddressList(self, rootAddress = None):
        if rootAddress is None:
            rootAddress = "."

        fileAddressList = list()

        for root, dirs, files in walk(rootAddress):
            for name in files:
                fileAddressList.append(path.join(root, name))
        return fileAddressList

    def updateSnowflakes(self, typeOfShowflake):
        dirPath = self.readConfig(typeOfShowflake, 'DIR')

        if dirPath == None:
            return 'Error'
        fileList = self.getFileAddressList(dirPath)

        for x in fileList:
            full_name = path.basename(x)
            name = path.splitext(full_name)[0]
            self.writeConfig(typeOfShowflake, name, full_name)

    def updateConf(self):
        fileList = self.getFileAddressList('conf')
        self.writeConfig("Snowflakes *.cfreezer", "path", fileList)

    def testVar(self):
        fileListFromConfig = self.getListFromConfig("Snowflakes *.*", "path")
        answer = ''

        if len(fileListFromConfig) > 0:
            answer = 'FileName\t\t\tAvailable\n'
            answer += '--------\t\t\t---------\n'
            for x in fileListFromConfig:
                answer += x + '\t\t' + str(path.isfile(x)) + '\n'
        else:
            answer = 'Files are not registered in the config.'
        return answer

    def update(self, whatToUpdate = None):
        if whatToUpdate is None:
            whatToUpdate = self.args[3]

        if whatToUpdate == 'snow':
            self.updateSnowflakes('Snowflakes *.html')
        elif whatToUpdate == 'py':
            self.updateSnowflakes('Snowflakes *.py')
        elif whatToUpdate == 'var':
            self.updateSnowflakes('Snowflakes *.*')
        elif whatToUpdate == 'conf':
            self.updateConf()
        elif whatToUpdate == 'all':
            self.updateSnowflakes('Snowflakes *.html')
            self.updateSnowflakes('Snowflakes *.py')
            self.updateSnowflakes('Snowflakes *.*')
            self.updateConf()

    def test(self, whatToTest = None):
        if whatToTest is None:
            whatToTest = self.args[3]

        answer = ''

        if whatToTest == 'var':
            answer = self.testVar()
        return answer

    def module_from_file(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def searchSnowflake(self, match, numberOfMargins=0):
        out = ''
        varName = match[1:match.find('@')] # <body.test@py@> -> body.test
        varNote = None

        if match.find('@') == match.rfind('@'):
            varNote = False
        else:
            varNote = match[match.find('@')+1:match.rfind('@')] # <body.test@py@> -> py

        a = 'varName = '+varName+'@'
        if varNote:
            a += str(varNote)
        print(a)
        
        if varNote == 'py':
            if self.configHasOption('Snowflakes *.py', varName):
                path = self.readConfig('Snowflakes *.py', 'DIR')+'/'+self.readConfig('Snowflakes *.py', varName)
                foo = self.module_from_file(varName, path)
                out += str(foo.freezer())
        elif varNote == 'var' or varNote == 'txt':
            if self.configHasOption('Snowflakes *.*', varName):
                path = self.readConfig('Snowflakes *.*', 'DIR')+'/'+self.readConfig('Snowflakes *.*', varName)
                with open(path, "r") as file:
                    s = file.readlines()
                for x in s:
                    out += ' '*numberOfMargins
                    out += x
        else:
            if self.configHasOption('Snowflakes *.html', varName):
                path = self.readConfig('Snowflakes *.html', 'DIR')+'/'+self.readConfig('Snowflakes *.html', varName)
                with open(path, "r") as file:
                    s = file.readlines()
                out += self.buildStrings(s, numberOfMargins)
        return out

    def buildString(self, string, numberOfMargins=0):
        x = string
        s_out = ""

        t = re.search(r'<[a-zA-Z0-9\.\@]*@>', x)

        s_out += ' '*numberOfMargins

        if t:
            start_space = 0
            space =  False
            end_space = 0
            for x1 in range(t.start()):
                if x[x1] == ' ':
                    start_space += 1

            if (start_space == t.start() and x[t.end()] == '\n') or (start_space == t.start()):
                var = str( self.searchSnowflake(t.group(), t.start()) )
            else:
                var = str( self.searchSnowflake(t.group()) )
                s_out += x[:t.start()]
            s_out += var
            s_out += x[t.end():]

            s_out = self.buildString(s_out)
        else:
            s_out = s_out + x

        return s_out

    def buildStrings(self, strings, numberOfMargins=0):
        s_out = ''

        for x in strings:
            s_out += self.buildString(x, numberOfMargins)
        return s_out

    def build(self):
        files = self.getFileAddressList('src')

        pathToStatic = self.readConfig('Static', 'DIR')
        pathToBuild = self.readConfig('Build', 'DIR')

        if path.isdir(pathToBuild):
            shutil.rmtree(pathToBuild)
            shutil.copytree(pathToStatic, pathToBuild+'/')
        else:
            shutil.copytree(pathToStatic, pathToBuild)

        for x in files:
            with open(x, "r") as file:
                s = file.readlines()
            out = self.buildStrings(s)
            p = pathToBuild+x[3:-len(path.basename(x))-1]
            p_t = pathToBuild+x[3:]

            if not path.isdir(p):
                mkdir(p)
            with open(p_t, "w") as file:
                file.write(out)
        
        
def main():
    f = Freezer(argv, getcwd())

    if argv[1] == 'start':
        f.startNewProject()
    else:
        if argv[2] == 'update':
            if len(argv) == 3:
                f.update("all")
            else:
                f.update()
        elif argv[2] == 'test':
            print(f.test())
        elif argv[2] == 'build':
            f.build()

if __name__ == "__main__":
    main() 
