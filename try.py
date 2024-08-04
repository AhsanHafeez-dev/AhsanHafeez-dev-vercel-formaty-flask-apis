import os 
import json
file =os.path.join("data","inserts.json")
with open(file,"r") as json_file:
            template=json.load(json_file)
            print(template)