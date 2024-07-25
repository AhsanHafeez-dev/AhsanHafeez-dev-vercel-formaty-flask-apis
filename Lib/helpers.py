from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex.utils import NoEscape , italic, bold , NoEscape
from pylatex import Document, Section, Subsection, Subsubsection, Command, Itemize, Enumerate, Table, Tabular
import json
import re


def demo():
    return "hello this is working"

def find_row_pattern(text):
    rows = re.findall(r"<tr>(.*?)</tr>", text, re.DOTALL) # Find all rows in the table
    if not rows:
        return "No rows found in the provided HTML content."

    max_columns = max((len(re.findall(r"<td.*?>", row)) for row in rows), default=0) # Find the maximum number of <td> elements in any row
        
    if max_columns == 0:
        return "No <td> elements found in the rows."

    # Generate the tabular definition based on max_columns
    tabular_definition = '|'.join(['c'] * max_columns)
    tabular_definition = f'|{tabular_definition}|'
    return tabular_definition


def handle_tables(text):

    # Replace <td colspan='x'>...</td> with \multicolumn{x}{|c|}{...} &
    pattern_td_colspan = r"<td colspan='(\d+)'>(.*?)</td>"
    replacement_td_colspan = r'\\multicolumn{\1}{|c|}{\2} & '
    text = re.sub(pattern_td_colspan, replacement_td_colspan, text)

    tabular_definition = find_row_pattern(text)

    text = re.sub(r"<td>(.*?)</td>", r'{\1} & ', text) # Replace <td>...</td> with {...} &
    text = re.sub(r'\n','', text) #removes new_line
    text = re.sub(r"<tr>", r' \n\\hline\n', text) # Replace <tr> with \hline
    text = re.sub(r"</tr>", '-1', text) # Replace </tr> with empty string
    text = re.sub(r'& -1','', text) #removes last row

    # Replace <table title='Table Caption' align='center'>
    pattern_table = r"<table title='(.*?)' align='center'>"    
    replacement_table = r'\n\\begin{table}[htbp]\n\\caption{\1}\n\\begin{center}\n\\begin{tabular}{%s}\n' % tabular_definition
    text = re.sub(pattern_table, replacement_table, text)
    text = re.sub(r"</table>", r'\n\\end{tabular}\n\\label{tab1}\n\\end{center}\n\\end{table}\n', text) # Replace </table>
    return text
    


def parse_content(text):
    text = handle_tables(text)
    text = text.replace("<b>", "\\textbf{").replace("</b>", "}")
    text = text.replace("<i>", "\\textit{").replace("</i>", "}")

    # Handle unordered lists
    text = text.replace("<ul>", "\\begin{itemize}").replace("</ul>", "\\end{itemize}")
    text = text.replace("<ol>", "\\begin{enumerate}").replace("</ol>", "\\end{enumerate}")

    # Handle list items
    text = text.replace("<li>", "\\item ").replace("</li>", "")
    text = re.sub(r"<cite>(.*?)</cite>", r'\\cite{\1}', text)
    text = re.sub(r"<cite type='paren'>(.*?)</cite>", r'\\parencite{\1}', text)


    # Handle images
    text = re.sub(r"<img src='(.*?)' alt='(.*?)' ?/?>", 
                  r'''
\\begin{figure}[htbp] 
\\centerline{\\includegraphics[width=\\linewidth]{\1}}
\\caption{\2}
\\label{fig:\1}
\\end{figure}''', text)


    
    
    return NoEscape(text)





def add_tables(doc, tables):
    for table in tables:
        with doc.create(Table(position='h')) as tab:
            tab.add_caption(table["caption"])
            tab.append(Command("centering"))
            with doc.create(Tabular('c' * len(table["data"][0]))) as tabular:
                tabular.add_hline()
                for row in table["data"]:
                    tabular.add_row(row)
                    tabular.add_hline()


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
    value = command.get("value", None)  # Use .get() for optional value

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


def fill_document(doc, data):
    for section in data["sections"]:
        with doc.create(Section(section["title"])):
            doc.append(parse_content(section["content"]))           
            # if "tables" in section:
            #     add_tables(doc, section["tables"])

            for subsection in section.get("subSections", []):
                with doc.create(Subsection(subsection["title"])):
                    doc.append(parse_content(subsection["content"]))


                    # if "tables" in subsection:
                    #     add_tables(doc, subsection["tables"])

                    for subsubsection in subsection.get("subSubSection", []):
                        with doc.create(Subsubsection(subsubsection["title"])):
                            doc.append(parse_content(subsubsection["content"]))
                            # if "tables" in subsubsection:
                            #     add_tables(doc, subsubsection["tables"])

def generate_author_block(authors):
    author_block = r'\author{'
    for i, author in enumerate(authors):
        author_block += r'\IEEEauthorblockN{' + str(i+1) + '. ' + author['userName'] + r'}' + '\n'
        author_block += r'\IEEEauthorblockA{\textit{' + author['department'] + r'} \\' + '\n'
        author_block += r'\textit{' + author['university'] + r'}\\' + '\n'
        author_block += author['city'] + r' \\' + '\n'
        author_block += author['email'] + r'}'
        if i < len(authors) - 1:
            author_block += r'\and' + '\n'
    author_block += r'}'
    return NoEscape(author_block)
