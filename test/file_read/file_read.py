import json
from types import SimpleNamespace

def escape_backslashes(input):
    return input.replace("\\\\", "\\")

# The classes used in serialization
class Sheet():

    def __init__(self, name, src, offX, offY, width, height):
        self.name = name
        self.src = src
        self.offX = offX
        self.offY = offY
        self.width = width
        self.height = height

    # Blank sheet
    def __init__(self, name):
        self.name = name
        self.src = ""
        self.offX = 0
        self.offY = 0
        self.width = 0
        self.height = 0

class Animation():
    def __init__(self, name):
        self.name = name
        self.dirs = 0
        self.sheet = ""
        self.shapeType = "Y_FLAT"
        self.flipX = []
        self.tileOffsets = []
        self.anchorOffsetX = []
        self.anchorOffsetY = []
        self.anchorOffsetZ = []
        self.time = 0
        self.repeat = []
        self.pivot = 0
        self.frames = []
        self.framesAlpha = []
        self.dirFrames = [[]]

# Declare operating consts
CC_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\CrossCode"
ANIM_FILE_PATH = CC_DIR + r"\assets\data\animations\player.json"

# Print operating consts
print(escape_backslashes(f"{CC_DIR = }"))
print(escape_backslashes(f"{ANIM_FILE_PATH = }"))

print()


# Animation Json processing code
##################################################

# Load the Json
anim_json = json.load(open(ANIM_FILE_PATH))
#print(anim_json_file)

# Check the DOCTYPE
if (anim_json["DOCTYPE"] != "MULTI_DIR_ANIMATION"):
    print("=== ERROR: Unsupported DOCTYPE")

else:

    print(f"dirs = {str(anim_json['dirs'])}")

    # Load the sheets
    print("Sheets")
    print("=" * 50)

    for sheet in anim_json["namedSheets"]:
        #print(f"{sheet} - {anim_json["namedSheets"][sheet]}")
        print(f"{sheet}")

    print()

    print("Animations")
    print("=" * 50)

    # SUB 1 - Grouped by sheets
    # SUB 2 - Grouped by fip/offsets
    # SUB 3 - Grouped by name
    for sub1 in anim_json["SUB"]:
        for sub2 in sub1["SUB"]:

            
            for sub3 in sub2["SUB"]:
                print(sub3)
                
                def remove_sub(json):
                    return_json = json
                    for i in return_json:
                        if (i == "SUB"):
                            return_json.pop(i)
                            break

                    return return_json

                print(remove_sub(sub2))
                print(remove_sub(sub1))
                print()
    
        break
        #for sub2 in sub1:
