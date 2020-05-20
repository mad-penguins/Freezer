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
        config.add_section("Snowflakes *.cfreezer")
        config['Snowflakes *.cfreezer']['path'] = str(list())

        with open(nameNewProject + '.freezer', "w") as config_file:
            config.write(config_file)

        mkdir("conf")
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

        for x in fileList:
            full_name = path.basename(x)
            index = full_name.find('.')

            if index != -1:
                full_name = full_name[:index]
            self.writeConfig("Snowflakes *.vfreezer", full_name, x)

        # config = configparser.ConfigParser()
        # config.read(self.args[1])
        # a = config.items('Snowflakes *.vfreezer')
        # print(a, type(a))
        # print(a[0][0], a[0][1], type(a[0][0]))

    def updateConf(self):
        fileList = self.getFileAddressList('conf')
        self.writeConfig("Snowflakes *.cfreezer", "path", fileList)

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
