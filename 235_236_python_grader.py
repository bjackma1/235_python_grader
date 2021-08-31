import json
import os

global unzipped_folder, output_filepath


class Student:

    def __init__(self, path):
        self.path = path
        path_len = len(unzipped_folder)
        self.name = path[path_len:(path_len + path[path_len:].index("_"))]
        self.html_notebook = ''
        self.student_cells = []

    def remove_images(self):
        """There are images in each ipynb file, and in the json, it's just the json representation of an image, which is
         just a bunch of characters, that starts with !"""
        if ".ipynb" in self.path:
            with open(self.path, 'r') as f:
                try:
                    student_json = json.load(f)
                    # cells are what the notebook is split up into
                    cells = student_json['cells']
                    for cell in cells:
                        for key in cell:
                            if key == 'source':
                                for row in cell[key]:
                                    try:
                                        if row[0] == "!" or row == "\n":
                                            cell[key].remove(row)
                                    except IndexError:
                                        pass
                    self.student_cells = cells
                except Exception as e:
                    print(e)
                    print(f"Check {self.name}'s submission manually")

    def parse_json_to_html(self):
        """ all this does is just return a formatted html-readable string that contains the json data.

            the two kinds of cells there are markdown and code. code cells contain both the source code and the
            output. """
        # each submission for a student is a div with an id of their name so that you can easily navigate to it from
        # the top
        self.html_notebook += f'<div id={self.name}><h3>{self.name}</h3>'
        for cell in self.student_cells:
            if cell['cell_type'] == 'markdown':
                markdown = ''
                for markdown_line in cell['source']:
                    markdown += markdown_line + '<br>'
                self.html_notebook += f'''
                <div class="markdown">
                    <str><em>Markdown for {self.name} </str></em><br>
                    {markdown}
                </div>'''
            elif cell['cell_type'] == 'code':
                source_code = ''
                code_output = ''
                for source_line in cell['source']:
                    source_code += '<pre>' + source_line + '<pre>'
                try:
                    # if there is no output we have to account for that and not break the html
                    for code_line in cell['outputs'][0]['text']:
                        code_output += '<pre>' + code_line + '</pre>'
                except IndexError as ie:
                    print(f'{ie} for {self.name}')
                self.html_notebook += f'''
                <div class="code">
                    <str><em>Code for {self.name} </str></em><br>
                    <code>{source_code}</code>
                </div>
                <div class="output">
                    <str><em>Output for {self.name} </str></em><br>
                    <pre>{code_output}</pre>
                </div>
                '''
        self.html_notebook += '</div>'


# file location may vary
def create_final_html(student_list):
    """gets all of the html for the students and adds buttons to navigate to everything and styles it. tbh the colors
       are kinda ugly so you can change them if you want"""
    final_html_list = ''

    style_element = '''
    <style>
        .code, .output  { font-family:"Lucida Console", Monaco, monospace; font-size:15px; }
        body            { font-size: 15px; background-color:#353535; color:white; }
        .markdown       { border: solid #F88D63 5px; font-family:Arial; background-color:#F56329; }
        .code           { border: solid #06D6A0 5px; background-color:#048B67; }
        .output         { border: solid #15ADE0 5px; background-color:#1082A8; }
        #name           { font-size: 40px; }
        #buttonGrid     { float: left }
        button          { width: 200px; background-color:#353535; border: none; background-color:"#353535" }
        h1              { position: sticky; top: 15px; }
        div             { width: auto; padding: 5px; margin:5px; word-wrap: break-word; }
        pre             { word-wrap: break-word; }
        a               { color: white; }
    </style>
    '''

    head_element = "<!DOCTYPE html><html><head><title>Python Homework</title>" + style_element + "</head><body>"

    final_html_list += head_element

    # button list allows you to click on an id and be instantly directed
    # to that student's submission
    buttons = '<div id="buttonGrid"><str>QUICK LINKS</str><br>'
    for i in range(len(student_list)):
        name = student_list[i].name
        buttons += f'<button><a href=#{name}>{name}</a></button>'

    buttons += "<br><br></div>"

    final_html_list += buttons

    # adding all html together
    for student in student_list:
        final_html_list += student.html_notebook

    final_html_list += '</body></html>'

    with open(output_filepath, 'w') as f:
        f.writelines(final_html_list)


def add_to_student_list(unzipped_folder_filepath):
    """creates a list of all student names and their corresponding Student() objects to be iterated over"""
    student_list = []
    for filename in os.listdir(unzipped_folder_filepath):
        path = unzipped_folder_filepath + filename
        student = Student(path)
        student.remove_images()
        student.parse_json_to_html()
        student_list.append(student)
    return student_list


def main():
    print(
        "In order for this program to work, the files have to be in an unzipped folder so you have to move them to"
        "\na regular folder"
    )

    global unzipped_folder, output_filepath
    unzipped_folder = input("Enter the path for the unzipped version of the folder: ") + "\\"
    output_filepath = input("Enter the path for the HTML file that you want to output: ")
    student_list = add_to_student_list(unzipped_folder)
    create_final_html(student_list)


if __name__ == '__main__':
    main()
