from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages
from pylatex import Document, Command,NoEscape
import database as db
import os
raw_preamble_list = [
  r"\DeclareLanguageMapping{american}{american-apa}",
  
  
]






def APA7( project_id):   
    
    content=db.get_project_content(project_id)
    # input("function execution started")
    
    templateName="APA7"
    doc_config,packages = db.get_template_info("APA7")
    preamble_list=db.get_project_preamable_list(project_id)
    
    # input("creating document")
    
    doc = Document(**doc_config)
    doc.append(Command("maketitle"))
    
    # input("created titile")
    
    fill_document(doc, content,templateName)

    doc.append(Command("printbibliography"))

    # input("start add raw preamable")
    add_raw_preamble(doc, raw_preamble_list)
    
    # input("end add raw preamable")

    # input("start add  preamable")
    # input(preamble_list)
    add_preamble(doc, preamble_list)
    # input("end add  preamable")

    # input("start add packages")
    # input(packages)
    add_packages(doc, packages)
    # input("end add packages")
    
    # input("generating tex")
    doc.generate_tex()
    # input("generating pdf")
    # doc.generate_pdf(os.path.join("temp","APA"), clean_tex=False)
    return "Successfully Generated APA Format"