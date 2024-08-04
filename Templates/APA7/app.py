from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages,download_all_images
from pylatex import Document, Command,NoEscape
import database as db
import os
raw_preamble_list = [
  r"\DeclareLanguageMapping{american}{american-apa}",
  
  
]






def APA7( project_id):       
    content=db.get_project_content(project_id)        
    templateName="APA7"
    doc_config,packages = db.get_template_info("APA7",project_id)
    preamble_list=db.get_project_preamable_list(project_id)
    keywords=db.get_key_words(preamble_list)        
    download_all_images(project_id)    
    doc = Document(**doc_config)
    doc.append(Command("maketitle"))   
    doc.append(NoEscape(f'\keywords{{{keywords}}}'))         
    fill_document(doc, content,templateName,project_id)
    doc.append(Command("printbibliography"))    
    add_raw_preamble(doc, raw_preamble_list)
    add_preamble(doc, preamble_list)   
    add_packages(doc, packages)
    doc.generate_tex()
    # doc.generate_pdf(os.path.join(os.path.join("temp",str(project_id)),"APA7"), clean_tex=False)
    input("see tex")
    path=os.path.join(os.path.join("temp",str(project_id)),"APA7")
    return [path+".tex","APA7.tex"]