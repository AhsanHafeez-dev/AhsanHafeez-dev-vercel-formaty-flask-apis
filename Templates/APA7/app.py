from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages
from pylatex import Document, Command
import database as db
raw_preamble_list = [
  r"\DeclareLanguageMapping{american}{american-apa}",
]


# Define your packages list
packages = [
  {"name": "babel", "options": ["american"]},
  {"name": "fontenc", "options": ["T1"]},
  {"name": "csquotes", "options": []},
  {"name": "biblatex", "options": ["style=apa", "sortcites=true", "sorting=nyt", "backend=biber"]},
  {"name": "mathptmx", "options": []},
]

doc_config = {
  {"name": "babel", "options": ["american"]},
  {"name": "fontenc", "options": ["T1"]},
  {"name": "csquotes", "options": []},
  {"name": "biblatex", "options": ["style=apa", "sortcites=true", "sorting=nyt", "backend=biber"]},
  {"name": "mathptmx", "options": []},
}



def APA7( project_id):   
    content=db.get_project_content(project_id)
    input("function execution started")

    doc_config,raw_preamble_list,packages = db.get_template_info("APA7")
    preamble_list=db.get_project_preamable_list(project_id)
    title,authorsList,abstract=db.get_project_preamable_list_info(project_id)
    preamble_list = [
        {"name": "addbibresource", "value": "bibliography.bib"},
        {"name": "title", "value": title['paperName']},
        {"name": "shorttitle", "value": title['shorttitle']},
        {"name": "author", "value": authorsList[0]['name']},
        {"name": "duedate", "value": "April 20, 2024"},
        {"name": "affiliation", "value": authorsList[0]['organization']},
        {"name": "course", "value": title['course']},
        {"name": "professor", "value": title['professor']},
        {"name": "abstract", "value": "This is the abstract for this paper, wherein the main points of the introduction, method, results, and discussion are quickly talked about. Probably in more than one sentence, though. Dare I guess, more than two? There is a page break before starting the Introduction."},
        ]
    input("creating document")
    doc = Document(**doc_config)
    doc.append(Command("maketitle"))
    input("created titile")
    
    fill_document(doc, content)

    doc.append(Command("printbibliography"))

    input("start add raw preamable")
    add_raw_preamble(doc, raw_preamble_list)
    input("end add raw preamable")

    input("start add  preamable")
    add_preamble(doc, preamble_list)
    input("end add  preamable")

    input("start add packages")
    add_packages(doc, packages)
    input("end add packages")
    input("generating tex")
    doc.generate_tex()
    input("generating pdf")
    doc.generate_pdf('output/APA7/output', clean_tex=False)
    return "Successfully Generated APA Format"