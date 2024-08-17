from Lib.helpers import fill_document, add_raw_preamble , add_preamble , add_packages,  generate_author_block_journal,download_all_images
from pylatex import Document, Command
from pylatex.utils import NoEscape
import database as db
import os 
from flask import send_file
raw_preamble_list = [
   r"\hyphenation{op-tical net-works semi-conduc-tor IEEE-Xplore}",
    # r"\IEEEoverridecommandlockouts",
]



def IEEEJournal(project_id):    
    templateName="IEEEJournal"
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
    print("all images downloaded")
    # input("getting content")
    content=db.get_project_content(project_id)
    # input("title template")
    title_template = NoEscape(r"""{paperName}*\\
    {{\footnotesize {footnotesize}}}
    """.format(paperName=title['paperName'], footnotesize=title['footnotesize']))    
    doc.append(Command('title', title_template))    
    
    # input("generting author block")
    author_block = generate_author_block_journal(authorsList, thanks=title['thanks'])    
    doc.append(author_block)    

    doc.append(NoEscape(r"\markboth{Journal of \LaTeX\ Class Files,~Vol.~14, No.~8, August~2021}"))
    doc.append(NoEscape(r"{Shell \MakeLowercase{\textit{et al.}}: "+title["paperName"] + r"}" ))
    

    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r"\begin{abstract}"))
    doc.append(abstract)
    doc.append(NoEscape(r"\end{abstract}"))
    doc.append(NoEscape(r"\begin{IEEEkeywords}"))
    doc.append(title["keywords"])
    doc.append(NoEscape(r"\end{IEEEkeywords}"))
        
    

    # input("fill document")
    
    fill_document(doc, content,templateName,project_id,True)
    
    
    # input("end full document")
    
    doc.append(NoEscape(r"\begin{IEEEbiographynophoto}{John Doe}"))
    doc.append(NoEscape(r"[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{image_5}}]{Michael Shell}"))
   #  appendices=db.get_appendices(project_id)
    appendices=db.get_project_content(project_id)
    
    doc.append(NoEscape(r"\appendices"))
    fill_document(doc, appendices,templateName,project_id,False)
    
    doc.append(NoEscape(r'\bibliographystyle{IEEEtran}'))
    doc.append(NoEscape(r'\bibliography{references}'))

    doc.generate_tex()
    print("creating for pdf for IEEE")
    # input("going for  pdf")
    file_path=os.path.join(os.path.join("temp",str(project_id)),"IEEEJournal")
    
    try:
      doc.generate_pdf(file_path, clean_tex=False)
      
    except Exception as e:
       print(e)
    
    return [file_path+".pdf","IEEE.pdf"]