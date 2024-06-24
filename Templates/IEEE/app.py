from Lib.helpers import demo
from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages, parse_content, generate_author_block
import json
from pylatex import Document, Command
from pylatex.utils import NoEscape

doc_config = {
    "default_filepath": "IEEE",
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

# List of authors
authors = [
    {
        'name': 'Given Name Surname',
        'department': 'dept. name of organization (of Aff.)',
        'organization': 'name of organization (of Aff.)',
        'city_country': 'City, Country',
        'email': 'email address or ORCID'
    },
    {
        'name': 'Given Name Surname',
        'department': 'dept. name of organization (of Aff.)',
        'organization': 'name of organization (of Aff.)',
        'city_country': 'City, Country',
        'email': 'email address or ORCID'
    },
    {
        'name': 'Given Name Surname',
        'department': 'dept. name of organization (of Aff.)',
        'organization': 'name of organization (of Aff.)',
        'city_country': 'City, Country',
        'email': 'email address or ORCID'
    },
    {
        'name': 'Given Name Surname',
        'department': 'dept. name of organization (of Aff.)',
        'organization': 'name of organization (of Aff.)',
        'city_country': 'City, Country',
        'email': 'email address or ORCID'
    }
]

json_data = '''{
    "title": "Demo Latex",
    "sections": [
        {
            "title": "Introduction",
            "content": "Lorem ipsum dolor sit amet, <ol><li>One</li><li>Two</li><li>Three</li></ol> <b>consectetur</b> adipisicing elit.Dolorem at ad cumque. Soluta architecto natus totam, <cite>Sample2024</cite> et sed delectus in.",
            "subSections": [
                {
                    "title": "Sub Introduction",
                    "content": "ello this",
                    "subSubSection": [
                        {
                            "title": "Sub Sub Introduction",
                            "content": "Lorem <b>ipsum</b> dolor sit amet,consectetur adipisicing elit. Dolorem at ad cumque. Soluta architecto natus totam, et sed delectus in.",
                            "endContent": "Lorem ipsum <i>dolor</i> sit amet, consectetur adipisicing elit. <b>Dolorem</b> at ad cumque. Soluta architecto natus totam, et sed delectus in."
                        }
                    ]
                }
            ]
        }
    ]
}'''




def IEEE(title):    
    data = json.loads(json_data)
    doc = Document(**doc_config)
    add_raw_preamble(doc, raw_preamble_list)
    add_packages(doc, packages)
    
    title_template = NoEscape(r"""{paperName}*\\
{{\footnotesize {footnotesize}}}
\thanks{{{thanks}}}
""".format(paperName=title['paperName'], footnotesize=title['footnotesize'], thanks=title['thanks']))
    doc.append(Command('title', title_template))
    author_block = generate_author_block(authors)
    doc.append(author_block)
    doc.append(NoEscape(r'\maketitle'))
    fill_document(doc, data)
    doc.generate_tex()
    doc.generate_pdf('IEEE', clean_tex=False)
    return "Successfully generated"