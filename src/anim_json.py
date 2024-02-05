'''
Copyright (c) 2024 Gregory Karastergios

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''


from util import escape_backslashes
import json
import settings
# Temporary code
#CC_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\CrossCode"
#ANIM_FILE_PATH = CC_DIR + r"\assets\data\animations\player.json"

def load_anim_file(anim_file_path):
    print(escape_backslashes(f"{settings.CC_DIR = }"))
    print(escape_backslashes(f"{anim_file_path = }"))

    print()

    # Animation Json processing code
    ##################################################

    # Load the Json
    anim_json = json.load(open(anim_file_path))
    #print(anim_json_file)

    # Check the DOCTYPE
    if (anim_json["DOCTYPE"] != "MULTI_DIR_ANIMATION"):
        print("=== ERROR: Unsupported DOCTYPE")

    else:

        print(f"dirs = {str(anim_json['dirs'])}")

        # Load the sheets
        print("Sheets")
        print("=" * 50)

        anim_list = []

        for sheet in anim_json["namedSheets"]:
            print(sheet)
            sheet_json = f"\"{sheet}\":{json.dumps(anim_json["namedSheets"][sheet])}"
            print(sheet_json)

            # sheet_list.append(json.loads(sheet_json)

        print()

        print("Animations")
        print("=" * 50)

        for sub1 in anim_json["SUB"]:
            for sub2 in sub1["SUB"]:

                # TODO: Make this part less crude
                if ("SUB" in sub2):
                    for sub3 in sub2["SUB"]:

                        # Remove the SUB object from the higher orders once separated
                        def remove_sub(json):
                            return_json = json
                            for i in return_json:
                                if (i == "SUB"):
                                    return_json.pop(i)
                                    break

                            return return_json

                        # Some jank to merge the SUBs together
                        anim_item_json = json.loads(json.dumps(sub3)[:-1] + ", " 
                                                    + json.dumps(remove_sub(sub2))[1:-1] + ", " 
                                                    + json.dumps(remove_sub(sub1))[1:])
                        print(anim_item_json)

                        anim_list.append(anim_item_json)

                        print()

                else:
                    anim_item_json = json.loads(json.dumps(sub2)[:-1] + ", " 
                                                    + json.dumps(remove_sub(sub1))[1:])
                    print(anim_item_json)

                    anim_list.append(anim_item_json)

                    print()
        
            return [anim_json["namedSheets"], anim_list]
                
            break