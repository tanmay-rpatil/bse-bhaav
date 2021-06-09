import argparse

# print ('#of args =', len(sys.argv), 'arguments.')
if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('echo',help='echo the string entered')
	args = parser.parse_args()
	print(args.echo)    
