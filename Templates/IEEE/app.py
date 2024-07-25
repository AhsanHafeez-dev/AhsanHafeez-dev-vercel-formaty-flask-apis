from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages, parse_content, generate_author_block
from pylatex import Document, Command
from pylatex.utils import NoEscape
import database as db
import os 

doc_config = {
    "default_filepath": "output/IEEE",
  "documentclass": "IEEEtran",
  "document_options": ["conference"],
  "fontenc": None,
  "inputenc": None,
  "lmodern": False,
  "textcomp": False,
    # "page_numbers" : False
}

# Define your packages list
packages = [
  {"name": "cite", "options": []},
  {"name": "amsmath", "options": []},
  {"name": "amssymb", "options": []},
  {"name": "amsfonts", "options": []},
  {"name": "algorithmic", "options": []},
  {"name": "graphicx", "options": []},
  {"name": "textcomp", "options": []},
  {"name": "xcolor", "options": []},
]

raw_preamble_list = [
    r"\IEEEoverridecommandlockouts",
]



def IEEE(project_id):
    input("IN IEEE ")
    
    doc_config,raw_preamble_list_2,packages =  db.get_template_info("IEEEa")
    
    input("initialized templates")
    doc = Document(**doc_config)

    add_raw_preamble(doc, raw_preamble_list)
    add_packages(doc, packages)
    input("done with  document initialization")

    print(type(project_id))
    input(project_id)
    title,authorsList,abstract = db.get_project_preamable_list_info(project_id)
    
    input("initialized preamable its")
    input(title)
    content=db.get_project_content(project_id)
    
    title_template = NoEscape(r"""{paperName}*\\
{{\footnotesize {footnotesize}}}
\thanks{{{thanks}}}
""".format(paperName=title['PaperName'], footnotesize=title['FootnoteSize'], thanks=title['Thanks']))
    
    doc.append(Command('title', title_template))
    input("set title")
    author_block = generate_author_block(authorsList)
    input("doc.append1")
    doc.append(author_block)
    input("doc.append2")
    doc.append(NoEscape(r'\maketitle'))
    input("done with authors")
    fill_document(doc, content)
    input("filled document")
    doc.generate_tex()
    
    doc.generate_pdf(os.path.join("temporary","IEEE"), clean_tex=False)
    return "Successfully generated"