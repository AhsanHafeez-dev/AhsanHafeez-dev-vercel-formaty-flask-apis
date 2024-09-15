
import os
import shutil
from flasgger import Swagger
from flask import request,jsonify,Flask,Response
app = Flask(__name__)
from flask_pymongo import PyMongo
import database as db
app.config["MONGO_URI"]="mongodb+srv://mbabarwaseem:579DFHzEn9dnrU3T@formatify-cluster.dvqcc9n.mongodb.net/test?retryWrites=true&w=majority&appName=formatify-cluster"
import pdf2bib
pdf2bib.config.set('verbose',False)
app.config['UPLOAD_FOLDER']='temp'
import bibtexparser
from werkzeug.utils import secure_filename

Swagger(app)


def get_bibtex_from_pdf(path):
    result=pdf2bib.pdf2bib(path)
    return result['bibtex']

@app.route("/templates",methods=['POST'])
def homePost():
    """
---
tags:
  - Templates
summary: Create a LaTeX document template
description: This endpoint creates a LaTeX document template based on the provided configuration.
parameters:
  - in: body
    name: body
    description: JSON payload containing the LaTeX document template configuration
    required: true
    schema:
      type: object
      properties:
        templateName:
          type: string
          example: IEEE
          description: The name of the template to be used
        documentclass:
          type: string
          example: IEEEtran
          description: The LaTeX document class to be used
        document_options:
          type: array
          items:
            type: string
          example: ["conference", "onecolumn"]
          description: Options for the LaTeX document class
        fontenc:
          type: string
          nullable: true
          example: null
          description: Font encoding option for the LaTeX document
        inputenc:
          type: string
          nullable: true
          example: null
          description: Input encoding option for the LaTeX document
        lmodern:
          type: boolean
          example: false
          description: Whether to use the lmodern package
        textcomp:
          type: boolean
          example: false
          description: Whether to use the textcomp package
        rawPreamables:
          type: array
          items:
            type: string
          example: ["r'\\IEEEoverridecommandlockouts'"]
          description: Raw LaTeX commands to be included in the preamble
        packages:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: cite
                description: The name of the LaTeX package
              options:
                type: array
                items:
                  type: string
                example: []
                description: Options for the LaTeX package
        keywords:
          type: array
          items:
            type: string
          example: ["phd thesis", "conferences", "book", "documentary"]
          description: Keywords associated with the LaTeX document
        description:
          type: string
          example: The IEEE (Institute of Electrical and Electronics Engineers) citation style is widely used in technical fields, especially in computer science and engineering. It is a numbered reference style that provides a consistent way to cite sources
          description: A description of the LaTeX document template
        publisher:
          type: string
          example: IEEE
          description: The publisher format of the document
        format:
          type: string
          example: IEEE
          description: The format of the document
        type:
          type: string
          example: IEEE
          description: The type of document being created
responses:
  200:
    description: LaTeX document template created successfully
  400:
    description: Invalid input data
"""

    # list of all templates to be inserted


    # jsons=["IEEE.json","APA7.json"]
    # jsons=[os.path.join(r"jsonTemplates","ACMConference")]

    # template=None
    
    
    # for file in jsons:
    #     with open(file,"r") as json_file:
    #         template=json.load(json_file)

    #     # if template is not available already insert it    
    #     if template is not None:
    #         db.save_to_database(template)
            


    #     template=None
    template=request.get_json()
    if template is None:
            data={"message":"there's nothing to insert"}
    else:
         db.save_to_database(template)
         data={"message":"Successfully inserted templates "}
        
    
    return jsonify(data), 200
    
    


@app.route("/templates",methods=["GET"])
def getAll():
    """
    templates route 
    ---
    tags:
      - Templates
    responses:
      200:
        description: Returns List of all available templates
"""

    return db.get_all_documents()



@app.route("/add-biblography",methods=["post"])
def add_biblography():
    
    # project_id=request.form.get('project_id')
    project_id="7583749385933957439"
    dump_folder=os.path.join("temp",str(project_id))
          
    if os.path.exists(dump_folder):
        shutil.rmtree(dump_folder)                
        print("deleted folder")
    else:
        print("folder doesnot exits before")  
    os.makedirs(dump_folder)
    file=request.files['file']

    if file.mimetype == 'application/pdf':
        if file.filename =='':
            return 'no files send'
        if file:
            print("got file")
            filename=secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], project_id,filename)
            file.save(file_path)

            bibtex_str=get_bibtex_from_pdf(file_path)
            # Parse the BibTeX content
            bib_database = bibtexparser.loads(bibtex_str)
            
            # Convert the BibTeX database to JSON
            bib_jsons = [entry for entry in bib_database.entries]
            id='3455fr65660'
            # id=db.add_bibtex_citations(bib_jsons[0])
            return id
            return f'File successfully uploaded to database'
    return "not a pdfs"

@app.route("/")
def home():
    return "welcome to formaty vercel apis"

if __name__=='__main__':
    app.run(debug=True)