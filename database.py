from flask_pymongo import PyMongo
from flask import jsonify
from app import app
from bson import  ObjectId
import os
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

def find_one(template_name):
    return db.templates.find_one({"templateName":template_name})

def get_all_project_info(project_id):        
    all_info=db.projects.find_one({"_id":project_id})    
    all_info.pop("_id")
    return all_info

def get_project_content(project_id):
    return get_all_project_info(project_id)["content"]

def get_project_images(project_id):
    return get_all_project_info(project_id)["images"]

def get_project_preamable_list_info(project_id):
    """ 
    Arguments : 
        - project_id : Type(str)
    Return : 
        - List of 3 elements
    Description : 
        - get all the project info based on project id and return list of title authorlist and abstract
    """
    project=get_all_project_info(project_id)    
    title=project["title"]
    authorsList=[]
    for author_id in project["authors"]:
        id=ObjectId(str(author_id))        
        author=db.users.find_one({"_id":id}) 
        # input(author)       
        author.pop("_id")
        authorsList.append(author)
    abstract=title["abstract"]
    title["keywords"]=",".join(title["keywords"])
    return [title,authorsList,abstract]

def get_template_info(template_name,project_id):
    """ 
    Arguments : 
        - templateName : Type(str)
        - project_id   : Type(syt)
    Return : 
        - List of 2 elements
    Description : 
        - get all the document initialization info and structured it into desired format and also specifying folder to save files
    """
    info=find_one(template_name)
    
    doc_config={
        "default_filepath": os.path.join(os.path.join("temp",str(project_id)),template_name),
        "documentclass"     :info [ "documentclass" ]   ,
        "document_options"   :info [ "document_options" ] ,
        "fontenc"           :info [ "fontenc" ]         ,       
        "lmodern"           :info [ "lmodern" ]         ,
        "textcomp"          :info [ "textcomp" ]
    }
    
    packages=info["packages"]
    return [doc_config,packages]

def add_sample_citations():                                                                         # this is temp function for generating sample citations
    """  
    write sample ciation to db it will be removed before pushing to production it is just for development and testing purposes
    """
    doc = {
    # "_id"     : ObjectId("60d5f3b7b7e6fbe5c56d3b2b")                    ,
    "type"    : "Journal Article"                                       ,                           # type is not part of .bib its just for our logic
    "Title"   : "A Study on Something"                                  ,                           # id would be replaces by this in html
    "Authors" : "John Doe, Jane Smith"                                  ,
    "Journal" : "International Journal of Studies"                      ,                           # follwing journal structure
    "Year"    : "2021"                                                  ,
    "Month"   : "June"                                                  ,
    "Day"     : "15"                                                    ,
    "Pages"   : "123-456"                                               ,
    "Volume"  : "10"                                                    ,
    "Issue"   : "2"
    }    
    db.citation.insert_one(doc)

def get_citation_json(citation_id):
    """ 
    accept citation_id and return json fetching from db on basis of id
    Warning : In case of citation not found return string message
    """
    try:
        citation=db.citation.find_one({"_id":citation_id}) 
    except Exception as e:
        print(e)      
    if citation:
        citation["_id"]=str(citation["_id"])
    else:
        return "citation not found"  
    return citation

def get_citation_title(citation_id):
    """ 
    Arguments : 
        - citaion_id : Type(str)
    Return : 
        - title : Type(str)
    Description : 
        - replace citation with its id so latex can map it from biblography file
    """
    citation_id=ObjectId(citation_id)
    info=db.citation.find_one({"_id":citation_id})
    if info:
        
        title=str(info["_id"])
        return title
    else:
        return "citation not found"
    
def get_all_citations(citation_id_list):
    """ 
    Arguments : 
        - citation_id_list : Type(str)
    Return : 
        - citations : Type(list)
    Description : 
        - fetch all citation in list and format it in format requuired by bibtexparser library
    """
    citations=[]
    for citation_id in citation_id_list:
        citation_id=ObjectId(citation_id)
        citation= db.citation.find_one({"_id":citation_id})        
        citation["_id"]=str(citation["_id"])                            
        citation["ID"]=citation["_id"]                                                      # bibtex parser library requies ID field
        citation.pop("_id")        
        citations.append(citation)    
    return citations

def get_project_preamable_list(project_id):    
    """ 
    Arguments : 
        - project_id : Type(str)
    Return : 
        - preamable_list : Type(list)
    Description : 
        - get all the preamable info and create a custom structured dictionary
    """
    title,authorsList,abstract=get_project_preamable_list_info(project_id)    
    preamble_list = [
        {"name": "addbibresource", "value": "references.bib"},
        {"name": "title", "value": title['paperName']},
        {"name": "shorttitle", "value": title['shorttitle']},
        {"name": "author", "value": authorsList[0]['userName']},
        {"name": "duedate", "value": "April 20, 2024"},
        {"name": "affiliation", "value": authorsList[0]['university']},
        {"name": "course", "value": title['course']},
        {"name": "professor", "value": title['professor']},
        {"name": "abstract", "value": abstract},
        {"name":"keywords","value":title["keywords"]}
        ]
    return preamble_list

def get_key_words(lst):
    return lst[-1]["value"]

def get_tenplate_name(project_id):
    return db.projects.find_one({"_id":project_id})["templateName"]