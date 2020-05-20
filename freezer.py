from os import getcwd
from sys import argv
import configparser
from os import mkdir, walk, path

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
        self.writeConfig("Source", "DIR", "src", nameNewProject+'.freezer')
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

    def test(self, whatToTest = None):
        if whatToTest is None:
            whatToTest = self.args[3]

        answer = ''

        if whatToTest == 'var':
            answer = self.testVar()
        return answer
        
        
def main():
    f = Freezer(argv, getcwd())

    if argv[1] == 'start':
        f.startNewProject()
    else:
        if argv[2] == 'update':
            f.update()
        elif argv[2] == 'test':
            print(f.test())

if __name__ == "__main__":
    main() 
