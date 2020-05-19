import configparser
from os import mkdir

class Freezer(object):
    """docstring for Freezer"""
    def __init__(self, args, workingDirectory):
        super(Freezer, self).__init__()
        self.args = args
        self.workingDirectory = workingDirectory


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

        with open(nameNewProject + '.freezer', "w") as config_file:
            config.write(config_file)

        mkdir("py")
        mkdir("snow")
        mkdir("src")
        mkdir("static")
        mkdir("vars")
        
            


        