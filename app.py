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
    templates route
    ---
    responses:
      200:
        description: Returns a simple message
    """
    
    # list of all templates to be inserted


    jsons=["IEEE.json","APA7.json"]

    template=None
    
    
    for file in jsons:
        with open(file,"r") as json_file:
            template=json.load(json_file)

        # if template is not available already insert it    
        if template is not None:
            db.save_to_database(template)
            


        template=None

    return "Successfully inserted templates "



@app.route("/templates",methods=["GET"])
def getAll():
    """
    templates route 
    ---
    responses:
      200:
        description: Returns List of all available templates
    """
    return db.get_all_documents()


@app.route("/create-paper", methods=["POST"])
def get_template():    

    """
    Process the template based on the provided template name and project ID.
    ---
    tags:
      - Template Processing
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - templateName
            - project_id
          properties:
            templateName:
              type: string
              description: The name of the template to be used.
              example: IEEE
            project_id:
              type: string
              description: The project ID to be processed.
              example: 60c72b2f9af1f145d4b7a123
    responses:
      200:
        description: Successfully processed the template
        schema:
          type: object
          properties:
            message:
              type: string
              description: The response message after processing the template
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message explaining what went wrong


    """
    data = request.get_json()
    # template_name = data.get('templateName')
    template_name="IEEE"
    project_id=ObjectId(data.get("project_id")) 

    if template_name:
        try:
            dump_folder="temp"
            try:
                shutil.rmtree(dump_folder)                
            except Exception as e:
                print("folder doesnot exits before")  
            os.makedirs(dump_folder)
            # db.add_sample_citations()
            # input("added sample citation to database")
            # input("in")       
            module = importlib.import_module(f"Templates.{template_name}.app")        
            # print("module imported")
            template_func = getattr(module, template_name)
            # print("function imported")
            response = template_func(project_id)          
            input("deleting folder")  
            shutil.rmtree(dump_folder)
            return jsonify({"message": response}), 200
        
        except (ModuleNotFoundError, AttributeError) as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "templateName not provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)

#