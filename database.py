from flask_pymongo import PyMongo
from flask import jsonify
from app import app

# app.config["MONGO_URI"]="mongodb+srv://ahsan:Hamza3755@templates.xrcj1en.mongodb.net/testing?retryWrites=true&w=majority&appName=templates"
app.config["MONGO_URI"]="mongodb+srv://mbabarwaseem:579DFHzEn9dnrU3T@formatify-cluster.dvqcc9n.mongodb.net/test?retryWrites=true&w=majority&appName=formatify-cluster"

db=PyMongo(app).db

def save_to_database(document):
    db.templates.insert_one(document)

def get_all_documents():
    """ 
    Arguments : 
        - None
    Return : 
        - documents : Type(json)
    Description : 
        - get all the avaaiable templates and return in form of json
    """
    cursor=db.templates.find({})
    documents=[]    
    for document in cursor:
        document["_id"]=str(document["_id"])
        documents.append( document   )    
    return jsonify(documents)

