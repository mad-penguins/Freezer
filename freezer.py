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
        config.read(nameConfig)

        if not config.has_section(section):
            config.add_section(section)
        config[section][option] = str(value)

        with open(nameConfig, "w") as config_file:
            config.write(config_file)

    def startNewProject(self, nameNewProject = None):
        if nameNewProject is None:
            nameNewProject = self.args[2]

        config = configparser.ConfigParser()

        config.add_section("Project")
        config.set("Project", "Name", nameNewProject)

        config.add_section("Source")
        config.set("Source", "dir", "src")

        config.add_section("Snowflakes *.html")
        config.add_section("Snowflakes *.py")
        config.add_section("Snowflakes *.vfreezer")
        config['Snowflakes *.vfreezer']['path'] = str(list())

        with open(nameNewProject + '.freezer', "w") as config_file:
            config.write(config_file)

        mkdir("py")
        mkdir("snow")
        mkdir("src")
        mkdir("static")
        mkdir("var")

    def getFileAddressList(self, rootAddress = None):
        if rootAddress is None:
            rootAddress = "."

        fileAddressList = list()

        for root, dirs, files in walk(rootAddress):
            for name in files:
                fileAddressList.append(path.join(root, name))
        return fileAddressList

    def updateVar(self):
        fileList = self.getFileAddressList('var')
        self.writeConfig("Snowflakes *.vfreezer", "path", fileList)
        #fileListFromConfig = self.getListFromConfig("Snowflakes *.vfreezer", "path")
        #print('fileList: ', fileList, len(fileList))
        #print('fileListFromConfig: ', fileListFromConfig, len(fileListFromConfig))
        #print(path.isfile(fileListFromConfig[0]))
        # with open(fileListFromConfig[0], "r") as c:
        #     print(c.read())

    def testVar(self):
        fileListFromConfig = self.getListFromConfig("Snowflakes *.vfreezer", "path")
        
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

        if whatToUpdate == 'var':
            self.updateVar()

    def test(self, whatToTest = None):
        if whatToTest is None:
            whatToTest = self.args[3]

        answer = ''

        if whatToTest == 'var':
            answer = self.testVar()
        return answer
        
        
            


        