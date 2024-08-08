import json
import os
import re
import shutil
from urllib.request import urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bson import ObjectId
from dotenv import load_dotenv
from pylatex import (Command, Document, Enumerate, Itemize, NewLine, Section,
                     Subsection, Subsubsection, Table, Tabular)
from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex.utils import NoEscape, bold, italic
from werkzeug.utils import secure_filename

import database as db

url_mapping={}
def demo():
    return "hello this is working"



def parse_content(doc,text,templateName,project_id):
    """" 
    Arguments
        - doc                  : Type(str)  html content to be parsed.
        - text                  : Type(str)  html content to be parsed.
        - templateName          : Type(str)  name of template for latex paper i.e IEEE/APA7 etc.
        - project_id            : Type(str)  project id for folder generation and fetching information 
    Return : 
        - None
    Description
    """
    
    
    
    # input("in parse content")
    text=add_tables(doc,text,templateName)                                                          # convert html table to latex tables            
    text = text.replace("<b>", "\\textbf{").replace("</b>", "}")                                    # replace b tag with \textbf(bold in latex)
    text=re.sub(r"(.*?)<sup>(.*?)</sup>",r"\1^{\2}",text)                                           # replace supSript tag wih ^ in latex (raise to or power)    
    text=re.sub(r"(.*?)<sub>(.*?)</sub>",r"\1_{\2}",text)                                           # replace SubScrpit tag with _ sub scrpit in latex
    text = text.replace("<i>", "\\textit{").replace("</i>", "}")                                    #replacing <i> with texttit (italic in latex)
    text = text.replace("<ul>", "\\begin{itemize}").replace("</ul>", "\\end{itemize}")             # Handle unordered lists
    text = text.replace("<ol>", "\\begin{enumerate}").replace("</ol>", "\\end{enumerate}")          # Handle orded lits
    text = text.replace("<li>", "\\item ").replace("</li>", "")                                     # Handle list items
    # input(text)
    text = re.sub(r"<p>(.*?)</p>", r"\1\n\n", text)                                                 # handling paragraph by replacing p tag with new line
    text = re.sub(r"<h.*?>(.*?)</h.*?>", r"\\textbf{\1}\n\n", text)                                 # handling heading in html by \textbf in latex
    # input(text)
    citation_ids=re.findall(r"<cite>(.*?)</cite>",text,re.DOTALL )                                  # getting all citation from database    
    if len(citation_ids)>0:                                                                         # if there is any citation
        # print("calling biblography")
        create_biblography_file(citation_ids,project_id)                                            # creating a biblography file 
            # Replace citation IDs with titles
    for citation_id in citation_ids:                                                        
        title = db.get_citation_title(citation_id)                                              # getting all tittles from citation ids 
        text = text.replace(f"<cite>{citation_id}</cite>", f"\\cite{{{title}}}")                # replace ids with title(obj id)
        # text = text.replace(f"<cite type='paren'>{citation_id}</cite>", f"\\parencite{{{title}}}")
    # text = re.sub(r"<cite>(.*?)</cite>", f'\\cite{get_citation_title(\1)}', text)
    # text = re.sub(r"<cite type='paren'>(.*?)</cite>", r'\\parencite{\1}', text)


    # Handle images
    # print("going for imags")
    text = re.sub(r'<img alt=(.*?) src=(.*?)>'
, replace_img_tag, text)     # Handle images
    # input(re.findall(r'<img alt=(.*?) src=(.*?)>',text,re.DOTALL))
    # input(text)
    # print("images")
    # print(re.findall(r"\\begin{figure}",txt,re.DOTALL))
    # print(text)    
    return NoEscape(text)

def add_tables(doc,html_content,templateName):
    """
    Input : 
        - html_content : Type(str)
        - templateName : Type(str)
    Return : 
        - LaTeX table
    docstring for function
  
    Output  LATEX_TABLE(Type : str)
    The functin takes string containing html table and transform to latex table using regular expressions
    Assumption : content or table data is plain text or number not a mathematical function or anything elinese
    Table does not include caption or centering
    """    

    
    soup=BeautifulSoup(html_content,"html.parser")
    thead=soup.find_all("thead")
    # input(thead)
    for head in thead:
        for td in head.find_all('td'):
            tag=soup.new_tag('b')
            tag.string=td.string
            td.string=""
            td.append(tag)
            # input(td)
    html_content=str(soup)
    # input(html_content)
    tables=re.findall("<table.*>.*?</table>",html_content,re.DOTALL)
    for table in tables:
        raw_table=table
        raw_table=re.sub(r"\n","",raw_table)
                
        if "APA" in templateName:
            tabular_defination,max_columns=get_tabular_defination_APA(raw_table)
        else:
            tabular_defination,max_columns = get_tabular_defination(raw_table)                  

        patterns = get_pattern_list()                                                                   #pattern to be matches                                                                                
        replace_with_list = get_replace_with_list(tabular_defination)                                   # replace with to go from html to latex
        if "APA" in templateName:
            replace_with_list[1]=r"\\multicolumn{\1}{c}{\2} &"
        
        for i in range(len(patterns)):  
            raw_table = re.sub(patterns[i], replace_with_list[i], raw_table)                # replace every html pattern with latex syntax
            # input(raw_table)

        raw_table=handle_multi_row(raw_table,max_columns)        
        
        
        html_content=html_content.replace(table,raw_table)
                # but still html
    # input(html_content)        
    return html_content



def add_packages(doc, packages):
  """
  Adds packages to a PyLaTeX document from a list of dictionaries.

  Args:
    doc: The PyLaTeX Document object.
    packages: A list of dictionaries where each dictionary defines a package:
              - name: The name of the package (str).
              - options (optional): A list of options for the package (str list).
  """
    
  for package in packages:
    doc.packages.append(Package(package["name"], options=package["options"]))


def add_preamble(doc, preamble_list):
  """
  Adds a list of commands to the preamble of a PyLaTeX document.

  Args:
    doc: The PyLaTeX Document object.
    preamble_list: A list of dictionaries where each dictionary defines a preamble command:
                  - name: The name of the command (str).
                  - value (optional): The value for the command (str).
  """
  for command in preamble_list:
            # Extract command name and value (if provided)
    name = command["name"]
    value = command.get("value", None)          # Use .get() for optional value

            # Append the command using Command class
    doc.preamble.append(Command(name, value))

def add_raw_preamble(doc, raw_preamble_list):
  """
  Adds a list of raw LaTeX commands to the preamble of a PyLaTeX document.

  Args:
    doc: The PyLaTeX Document object.
    raw_preamble_list: A list of strings containing raw LaTeX code.
  """
  for raw_preamble in raw_preamble_list:
    doc.preamble.append(NoEscape(raw_preamble))


def fill_document(doc, data,templateName,project_id):
    """ 
    Input : 
        - doc            : Type(str)
        - data           : Type(str)
        - templateName   : Type(str)
        - project_id     : Type(str)
    Return : 
        - None

    Description:
        - add the content to LaTeX document
        - handle section subsection and sub sub section
    """
    
    
            # input(data)
    for section in data["included"]:
        with doc.create(Section(section["title"])):
            print("Sections")

            content=parse_content(doc,section["content"],templateName,project_id)
            doc.append(content)

            for subsection in section.get("subSections", []):
                with doc.create(Subsection(subsection["title"])):
                    doc.append(parse_content(doc,subsection["content"],templateName,project_id))


                    for subsubsection in subsection.get("subSubSections", []):
                        with doc.create(Subsubsection(subsubsection["title"])):
                            doc.append(parse_content(doc,subsubsection["content"],templateName,project_id))
                
    
    

def generate_author_block(authors):

    
    author_block = r'\author{'
    for i, author in enumerate(authors):
        if author['userName']=='':
            author['userName']="please enter User Name"
        if author['department']=='':
            author['department']="please enter department Name"
        if author['university']=='':
            author['university']="please enter university Name"
        if author['city']=='':
            author['city']="please enter city Name"        
        if author['email']:
            author['email']="please enter email"
        author_block += r'\IEEEauthorblockN{' + str(i+1) + '. ' + author['userName'] + r'}' + '\n'
        author_block += r'\IEEEauthorblockA{\textit{' + author['department'] + r'} \\' + '\n'
        author_block += r'\textit{' + author['university'] + r'}\\' + '\n'
        author_block += author['city'] + r' \\' + '\n'
        author_block += author['email'] + r'}'
        if i < len(authors) - 1:
            author_block += r'\and' + '\n'
    author_block += r'}'
    return NoEscape(author_block)


def create_biblography_file(citation_id_list,project_id=""):       
            # print("biblography")
    
    lst_of_citations = db.get_all_citations(citation_id_list)

    bib_db=BibDatabase()
    bib_db.entries=lst_of_citations
    bib_str=bibtexparser.dumps(bib_db) 
    
    with open(os.path.join(os.path.join("temp",str(project_id)),"references.bib"),'w') as bib_file:
        bib_file.write(bib_str)


            # writer = BibTexWriter()
            # writer.indent = '    '            # indent entries with 4 spaces instead of one
            # writer.comma_last = True          # place the comma at the beginning of the line
            # with open('temp/references.bib', 'w') as bibfile:
            #     bibfile.write(writer.write(bib_db))        
        
        
def get_pattern_list():
        """ 
    Input : 
        - None
    Output : 
        - rpattern : Type(list)
    Description:
        - patterns to be replaces to go from html to latex
    """
        
                                                                                    #pattern to be matches
        patterns = [
            
            r"<td colspan=\"(\d+)\">(.*?)</td>"     ,                                   #1  merging colum or colinespan handling
            r"<td rowspan=\"(\d+)\">(.*?)</td>"     ,                                   #2  hadling of row merging or rowsapn
            r"<td>(.*?)</td>"                       ,                                   #3  normal column and data
            r"\n"                                   ,                                   #4  new line character
            r"<tr>"                                 ,                                   #5  start of row
            r"</tr>"                                ,                                   #6  end of row
            r"<cite>(.*?)</cite>"                   ,                                   #7  citations    
            r"&\s*-1"                               ,                                   #8  extra & -1 sign at end of each row
            r"</table>"                             ,                                   #9  end of table tage
            r"<table.*?>"                           ,                                   #10 start table tag
            r"<.*?thead>"
        ]

                                                                                        # replace with to go from html to latex
        
        return patterns
def get_replace_with_list(tabular_defination):
    """ 
    Input : 
        - tabular_defination : Type(str)
    Output : 
        - replace_with_list : Type(list)
    Description:
        - replacement to be made to go from html to latex
    """
    replace_with_list = [
            r"\\multicolumn{\1}{|c|}{\2} &"         ,                                   #1  latex syntax for meging colum {no_of_colums}{|c|}{content}
            r"\\multirow{\1}{*}{\2} &"              ,                                   #2  latex syntax for meging colum {no_of_rows}{*}{content}
            r"\1 &"                                 ,                                   #3  adding data and & to express sepration of column
            r""                                     ,                                   #4  as we dont need extra new lines we will just remove it
            r""                                     ,                                   #5  before adding each row we will draw horizontol line and add new line
            r"-1 \\\\\n\\hline\n"                   ,                                   #6  -1 is used as flag signaling the end of row for removing extra things at end
            r"\\cite{\1}"                           ,                                   #7  replace citations with latex syntax of \cite {citation name}
            r""                                     ,                                   #8  now removing extra & and -1 sign at end of each row
            r"\n\\end{tabular}\n\\label{table}\n\\end{center}\n\\end{table}\n"                   ,                                  #9  latex syntax signaling end of table
            r'\n\\begin{table}[htbp]\n\\caption{Sample Caption}\n\\begin{center}\n\\begin{tabular}{' + tabular_defination + r'}\n\\hline\n'  ,              #10 latex syntax signaling start of table
            r""
        ]
    
    
    return replace_with_list
def get_tabular_defination(table):
        """ 
        Input : 
            - table : Type(str)
        Description : 
            - takes html table and create latex table defination from it e.g |c|c|c|
            
        Return :
            - tabular_defination : Type(str)
        """
        rows = re.findall(r"<tr>(.*?)</tr>", table, re.DOTALL)
                                                                                        # finding maximum number of columns  for use in tabular defination i.e {c|c|}
        max_columns = max((sum(1 for _ in re.finditer(r"<td.*?>", row)) for row in rows), default=0)
        
                                                                                        # setting latex syntax regading how many columns will be in column
        tabular_defination = '|'.join('c' * max_columns)
        tabular_defination = f"|{tabular_defination}|"
        get_tabular_defination_APA(table)
        return [tabular_defination,max_columns]

def get_tabular_defination_APA(table):
        
        """ 
        Input : 
            - table : Type(str)
        Description : 
            - takes html table and create latex table defination from it e.g |c|c|c|
        Return :
            - tabular_defination : Type(str)
            - in APA7 we dont draw vertical lines so no need to add '|'
        """
        rows = re.findall(r"<tr>(.*?)</tr>", table, re.DOTALL)
                                                                                        # finding maximum number of columns  for use in tabular defination i.e {c|c|}
        max_columns = max((sum(1 for _ in re.finditer(r"<td.*?>", row)) for row in rows), default=0)
        
                                                                                        # setting latex syntax regading how many columns will be in column
        tabular_defination = ''.join('c' * max_columns)
        tabular_defination = f"{tabular_defination}"
        
      
        return [tabular_defination,max_columns]


def handle_multi_row(table,max_columns):
        """      
        Input : 
            - table         : Type(str)
            - max_colums    : Type(str)
        Description :
            - takes in latex table and replace hline with hhline in case of multirow column
        """
    
        if r"\multirow" not in table:
            return 
        lines=table.split("\n")                                                         # getting all lines in table
                                                     
        for i in range(len(lines)):
            if r"\multirow" in lines[i]:                                                # handling of multirows
        
                match = re.search(r"\\multirow{(\d+)}", lines[i])                       # capture the match object
                if match:
                    rows = int(match.group(1))                                          # how many rows will it occupy
                    
                    for replace in range(i + 1, i + 1 + rows,2):                        # on each next line write \\hhline
        
                        lines[replace] = r"\hhline{~" + '-' * (max_columns - 1) + "}"   # replaces \hline with \hhline {~-(max column times)}
        
            lines[i] += "\n"                                                            # when splitting we deleted \n character now insert it again 
        table="".join(lines)                                                            # convert the list into string again
        return table

def download_all_images(project_id):
    """ 
    Input : 
        - project_id : Type(str)
    fetch the image list from database based on project id and install the images
    """
    
    img_url_lst=db.get_project_images(project_id)
    # img_url_lst=["https://media.geeksforgeeks.org/wp-content/uploads/20210224040124/JSBinCollaborativeJavaScriptDebugging6-300x160.png" ]
    i=1
    
    for image_url in img_url_lst:
        parsed_url = urlparse(image_url)
        path = parsed_url.path
        file_ext = os.path.splitext(path)[-1].lower()
        filename=f'image_{str(i)}{file_ext}'
        
        path=os.path.join(os.path.join("temp",str(project_id)),filename  )
        url_mapping[image_url]=filename
        urlretrieve(image_url, path)
        i+=1
    

def get_image_name(url):
    """ 
    Input:
        - url  : Type(str) 
    Description:
        -map name to url
    """
    return url_mapping[url]  
def replace_img_tag(match):
    """ 
    Input :
        - match  re.compile
    Description:
        - latex code for showing image
    """
    # input("match")
    url = match.group(2).strip('"/"')
    alt = match.group(1)
    # input(url_mapping)
    image_name = get_image_name(url)
    figure="figure"
    # input("dshkehgiregire")
    width="375pt"
    height="375pt"
    return f'''
    \\begin{{{figure}}}[htbp] 
    \\centerline{{\\includegraphics[width=\\linewidth]{{{image_name}}}}}
    \\caption{{{alt}}}
    \\label{{fig:{image_name}}}
    \\end{{{figure}}}'''    


        #end of helper