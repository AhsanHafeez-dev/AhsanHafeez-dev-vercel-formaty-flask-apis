from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages, parse_content, generate_author_block
from pylatex import Document, Command
from pylatex.utils import NoEscape

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



def IEEE(title, authorsList, content):
    doc = Document(**doc_config)
    add_raw_preamble(doc, raw_preamble_list)
    add_packages(doc, packages)
    
    title_template = NoEscape(r"""{paperName}*\\
{{\footnotesize {footnotesize}}}
\thanks{{{thanks}}}
""".format(paperName=title['paperName'], footnotesize=title['footnotesize'], thanks=title['thanks']))
    doc.append(Command('title', title_template))
    author_block = generate_author_block(authorsList)
    doc.append(author_block)
    doc.append(NoEscape(r'\maketitle'))
    fill_document(doc, content)
    doc.generate_tex()
    doc.generate_pdf('output/IEEE', clean_tex=False)
    return "Successfully generated"