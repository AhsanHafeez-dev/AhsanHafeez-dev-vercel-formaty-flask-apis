from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages, parse_content, generate_author_block,download_all_images
from pylatex import Document, Command
from pylatex.utils import NoEscape
import database as db
import os 

raw_preamble_list = [
    r"\IEEEoverridecommandlockouts",
]



def IEEE(project_id):    
    templateName="IEEE"
    doc_config,packages =  db.get_template_info(templateName)
    doc = Document(**doc_config)
    add_raw_preamble(doc, raw_preamble_list)
    add_packages(doc, packages)    
    title,authorsList,abstract = db.get_project_preamable_list_info(project_id)
    download_all_images(project_id)
    # input(title)
    content=db.get_project_content(project_id)
    
    title_template = NoEscape(r"""{paperName}*\\
    {{\footnotesize {footnotesize}}}
    \thanks{{{thanks}}}
    """.format(paperName=title['paperName'], footnotesize=title['footnotesize'], thanks=title['thanks']))    
    doc.append(Command('title', title_template))    
    author_block = generate_author_block(authorsList)    
    doc.append(author_block)    
    doc.append(NoEscape(r'\maketitle'))    
    fill_document(doc, content,templateName)
    

    doc.generate_tex()
    print("going for pdf")
    try:
      doc.generate_pdf(os.path.join("temp","IEEE"), clean_tex=False)
      
    except Exception as e:
       print(e)
    return "Successfully generated"