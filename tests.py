import util3 as util
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

etaData = util.load(DATA_FOLDER / "etaData.json")
print(etaData[util.dKey([4,2,2])])