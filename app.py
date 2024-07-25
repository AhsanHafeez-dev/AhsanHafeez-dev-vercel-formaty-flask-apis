from flask import Flask, request, jsonify
from flasgger import Swagger
from bson import  ObjectId
import importlib
import json
import os
import shutil 

app = Flask(__name__)
import database as db



Swagger(app)

@app.route("/templates", methods=["POST"])
def homePost():
    """
    Home route
    ---
    responses:
      200:
        description: Returns a simple message
    """
    
    # list of all templates to be inserted
    jsons=["APA7.json","IEEE.json"]
    template=None
    
    
    for file in jsons:
        with open(file,"r") as json_file:
            template=json.load(json_file)

        # if template is not available already insert it    
        if template is not None:
            db.save_to_database(template)
            


        template=None

    return "Successfully inserted templates "



@app.route("/getAll",methods=["GET"])
def getAll():

    return db.get_all_documents()

@app.route("/template", methods=["POST"])
def get_template():
    
    input("got request")
    data = request.get_json()
    input("got json")
    template_name = data.get('templateName')
    project_id=ObjectId(data.get("project_id"))
    
    all_data=db.find_one( template_name )
    
 
    input("going for if")
    

    if template_name:
        try:
            # dump_folder="temporary"
            # try:
            #     shutil.rmtree(dump_folder)
                
            # except Exception as e:
            #     os.makedirs(dump_folder)
            #     print("folder doesnot exits")
            
            input("got name ")
            
            module = importlib.import_module(f"Templates.{template_name}.app")
            input("Module imported")
            template_func = getattr(module, template_name)
            print(template_func)
            input("got functiom")
            response = template_func(project_id)
            input("response returning and deleting temp")

            # shutil.rmtree(dump_folder)
            return jsonify({"message": response}), 200
        
        except (ModuleNotFoundError, AttributeError) as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "templateName not provided"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
