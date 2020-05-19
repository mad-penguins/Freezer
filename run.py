import configparser
from os import getcwd
from sys import argv
from freezer import Freezer

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "font", "Courier")
    config.set("Settings", "font_size", "10")
    config.set("Settings", "font_style", "Normal")
    config.set("Settings", "font_info",
                "You are using %(font)s at %(font_size)s pt")

    test = ["test1","test2","test3","test4"]

    config.add_section("Path to templates files")
    config['Path to templates files']["test1"] = str(test)
    #config['Path']["test2"]
    #config['Path']["test3"]
    #print(config)
    #print(type(config))
    #config.set("Path","test", None)
    #config.set("Path","test1", None)
    
    with open(path, "w") as config_file:
        config.write(config_file)


def main():
	f = Freezer(argv, getcwd())

	if argv[1] == 'start':
		f.startNewProject()



if __name__ == "__main__":
    # path = "project11.freezer"
    # createConfig(path)
    main()