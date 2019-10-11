import util3 as util


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")


"""
start with 2x2 seed - have some way of tracking progress
for each g in G get L (don't need to do l max,max) 
go through square cases and establish eta
go through non-square cases
do any manual eta if necessary
continue

"""



def main():
	index = getIndex()
	#data of form {node : eta}
	data = util.load(DATA_FOLDER / "graph.json")


def getIndex():
	pass

def seed():
	pass




if __name__ == "__main__":
	main()