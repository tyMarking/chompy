import cProfile
import pstats
import etaExpansion as etaexp
from pathlib import Path
import os

cProfile.run("etaexp.profileIt()", "etaStats")

THIS_FOLDER = Path(etaexp.THIS_FOLDER)
fileName = THIS_FOLDER / "profile.txt"

with open(fileName, 'w') as stream:
	p = pstats.Stats('etaStats', stream=stream)
	p.sort_stats('cumulative')
	p.print_stats()
