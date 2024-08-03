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
    # input("getting template info")
    doc_config,packages =  db.get_template_info(templateName,project_id)
    # input("initiazlizing document")
    doc = Document(**doc_config)
    # input("adding rw preamable")
    add_raw_preamble(doc, raw_preamble_list)
    # input("add packages")
    add_packages(doc, packages)    
    # input("getting preamable list info")
    title,authorsList,abstract = db.get_project_preamable_list_info(project_id)
    
    download_all_images(project_id)
    # input("getting content")
    content=db.get_project_content(project_id)
    # input("title template")
    title_template = NoEscape(r"""{paperName}*\\
    {{\footnotesize {footnotesize}}}
    \thanks{{{thanks}}}
    """.format(paperName=title['paperName'], footnotesize=title['footnotesize'], thanks=title['thanks']))    
    doc.append(Command('title', title_template))    
    # input("generting author block")
    author_block = generate_author_block(authorsList)    
    doc.append(author_block)    

    doc.append(NoEscape(r'\maketitle'))
    
    doc.append(NoEscape(r"\begin{abstract}"))
    doc.append(abstract)
    doc.append(NoEscape(r"\end{abstract}"))
    doc.append(NoEscape(r"\begin{IEEEkeywords}"))
    doc.append(title["keywords"])
    doc.append(NoEscape(r"\end{IEEEkeywords}"))
        
    

    # input("fill document")
    fill_document(doc, content,templateName,project_id)
    # input("end full document")
    doc.append(NoEscape(r'\bibliographystyle{plain}'))
    doc.append(NoEscape(r'\bibliography{references}'))

    doc.generate_tex()
    print("creating for pdf for IEEE")
    # input("going for  pdf")
    try:
      doc.generate_pdf(os.path.join(os.path.join("temp",str(project_id)),"IEEE"), clean_tex=False)
      
    except Exception as e:
       print(e)
    return "Successfully generated"