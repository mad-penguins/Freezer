from settings import content
from settings import title
from settings import address_file

from head_open import head_open
from meta_open import meta_open
from meta_close import meta_close
from head_close import head_close
from body_open import body_open
from header import header
from mad_head import mad_head
from slider import slider
from main_open import main_open
from main_close import main_close
from footer import footer
from body_close import body_close

from main_index import main_index

code = ""

def gen_index():
	global code
	code += head_open
	code += meta_open
	code += content
	code += meta_close
	code += title
	code += head_close
	code += body_open
	code += header
	code += mad_head
	code += slider
	code += main_open

	code += main_index

	code += main_close
	code += footer
	code += body_close

	#print(code)
	f = open(address_file+"index.html", 'w')
	f.write(code)
	f.close()

def main():
	command = str(input("Enter command: "))
	if command == "generate":
		command_gen = str(input("file?:"))
		if command_gen == "index":
			gen_index()

if __name__ == '__main__':
	main()