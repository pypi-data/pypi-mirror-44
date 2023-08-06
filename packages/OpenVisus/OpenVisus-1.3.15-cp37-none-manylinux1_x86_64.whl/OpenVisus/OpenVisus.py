import sys,os

__this_dir__=os.path.dirname(os.path.abspath(__file__))

OpenVisusDir=__this_dir__

for it in (".","bin"):
	dir = os.path.join(__this_dir__,it)
	if not dir in sys.path and os.path.isdir(dir):
		sys.path.append(dir)

# soon or later all these will be packages
from VisusKernelPy import *
	
try:
	from VisusDataflowPy import *
except:
	pass
	
try:
	from VisusDbPy import *
except:
	pass
	
try:
	from VisusIdxPy import *
except:
	pass
	
try:	
	from VisusNodesPy import *
except:
	pass

VISUS_GUI=False
try:
	from VisusGuiPy import *
	VISUS_GUI=True
except:
	pass
	
try:
	from VisusGuiNodesPy import *
except:
	pass
	
try:
	from VisusAppKitPy import *
except:
	pass

try:
	from VisusXIdxPy import *
except:
	pass



