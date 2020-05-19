from os import getcwd
from sys import argv
from freezer import Freezer

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