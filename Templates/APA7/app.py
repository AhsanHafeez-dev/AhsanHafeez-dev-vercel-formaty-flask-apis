from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages
from pylatex import Document, Command

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
  "default_filepath": "output/APA7/output",
  "documentclass": "apa7",
  "document_options": ["stu", "12pt", "floatsintext"],
  "fontenc": None,
  "inputenc": None,
  "lmodern": False,
  "textcomp": False,
}



def APA7(title,authorsList , content):   
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

    doc = Document(**doc_config)
    doc.append(Command("maketitle"))
    fill_document(doc, content)
    doc.append(Command("printbibliography"))
    add_raw_preamble(doc, raw_preamble_list)
    add_preamble(doc, preamble_list)
    add_packages(doc, packages)
    doc.generate_tex()
    doc.generate_pdf('output/APA7/output', clean_tex=False)
    return "Successfully Generated APA Format"