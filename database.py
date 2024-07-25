from flask_pymongo import PyMongo
from flask import jsonify
from app import app
import json
from bson import  ObjectId
import os
# app.config["MONGO_URI"]="mongodb+srv://ahsan:Hamza3755@templates.xrcj1en.mongodb.net/testing?retryWrites=true&w=majority&appName=templates"
app.config["MONGO_URI"]="mongodb+srv://mbabarwaseem:579DFHzEn9dnrU3T@formatify-cluster.dvqcc9n.mongodb.net/test?retryWrites=true&w=majority&appName=formatify-cluster"

db=PyMongo(app).db

def save_to_database(document):
    db.templates.insert_one(document)

def get_all_documents():
    
    cursor=db.templates.find({})
    documents=[]
    
    for document in cursor:
        print(document["_id"])
        input("have you compared id")
        inserted_document={"docConfig":document["docConfig"],"rawPreamables":document["rawPreamables"],"packages":document["packages"]}
        
        documents.append( inserted_document   )        
    
    return jsonify(documents)

def find_one(template_name):
    return db.templates.find_one({"templateName":template_name})

def get_all_project_info(project_id):
    
    
        
    all_info=db.projects.find_one({"_id":project_id})
    print(all_info)
    all_info.pop("_id")
    return all_info

def get_project_content(project_id):
    return get_all_project_info(project_id)["content"]

def get_project_preamable_list_info(project_id):

    project=get_all_project_info(project_id)
    input("got project")
    title=project["title"]
    authorsList=[]
    for author_id in project["authors"]:
        id=ObjectId(str(author_id))
        author=db.users.find_one({"_id":id})
        author.pop("_id")
        authorsList.append(author)


    abstract=project["abstract"]
    return [title,authorsList,abstract]

def get_template_info(template_name):
    info=find_one(template_name)
    input(info)
    doc_config={
        "default_filepath": os.path.join("temporary","IEEE"),
        "documentclass"     :info [ "documentclass" ]   ,
        "document_options"   :info [ "document_options" ] ,
        "fontenc"           :info [ "fontenc" ]         ,
        "inputenc"          :info [ "inputenc" ]        ,
        "lmodern"           :info [ "lmodern" ]         ,
        "textcomp"          :info [ "textcomp" ]


    }
    raw_preamable_list=info["rawPreamables"]
    print("class : ",info["documentclass"])
    packages=info["packages"]
    return [doc_config,raw_preamable_list,packages]

