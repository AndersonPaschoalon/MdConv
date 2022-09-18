import time
import markdown
import os
import traceback
import sys
import getopt
from os.path import exists
from htmldocx import HtmlToDocx
import random
import pdfkit

"""
TODO
1. conv to pdf
2. conv to txt
3. release
"""

class Md:
    HTML_HEADER = """<html>
<head>
  <meta http-equiv="Content-Type" content="utf-8">
  <title>###THE_TITLE###</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> 
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
body {
  font-family: 'Helvetica', 'Arial', sans-serif;
  max-width: 767px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 10px;
  padding-right: 10px;
}

h1 {
  font-weight: bold;
  font-size: 22px;
  margin: 20px 0;
  text-align: left;
}
h2 {
  font-weight: bold;
  font-size: 18px;
  margin: 20px 0;
  text-align: left;
}
h3 {
  font-weight: bold;
  font-size: 16px;
  margin: 20px 0;
  text-align: left;
}
h4 {
  font-weight: bold;
  font-size: 15px;
  margin: 20px 0;
  text-align: left;
}
h5 {
  font-size: 14px;
  margin: 20px 0;
  text-align: left;
}
h6 {
  font-size: 13px;
  margin: 20px 0;
  text-align: left;
}
p {
    margin: 10px 0;
    padding: 5px;
	font-size: 12px;
}
code{
    padding: 5px;
	color: black
}
    </style>
</head>
<body>
"""
    HTML_FOOTER = """</body>
</html>
"""

    @staticmethod
    def html_file(md: str, filename: str, title=""):
        html = Md.html_str(md, title)
        with open(filename, 'w+') as f:
            f.write(html)
        return True

    @staticmethod
    def html_str(md: str, title=""):
        html = Md.HTML_HEADER.replace("###THE_TITLE###", title)
        html += markdown.markdown(md)
        html += Md.HTML_FOOTER
        html.replace('’', '\'')
        return html


class Main:

    RET_ERROR_INVALID_ARGS = 1
    RET_ERROR_PARSING_ARGS = 2
    RET_ERROR_FILE_NOT_FOUND = 3
    RET_ERROR_EXCEPTION_PROCESSING_FILES = 4
    RET_ERROR_GENERIC = 5
    RET_INVALID_FORMAT = 6
    # rc-v: release candidate version
    # v: stable version
    APP_VERSION = "rc-v1.0.1.0"
    LICENSE = """
MIT License

Copyright (c) 2022 Anderson Paschoalon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.    
    """
    APP_MANPAGE = """
    NAME
        MdConv.exe - an app to convert md files into different formats.

    USAGE
        mdconv.exe --md <markdown-file> --title <html-title>
        mdconv.exe --md <markdown-file> --title <html-title> --output <output-format>
        mdconv.exe --help
        mdconv.exe --version
        mdconv.exe --license

    OPTIONS
        -m <md-file>, --md=<md-file>
            Path to the Markdonw file to be converted into the specified format. 
            Default format is HTML.
        -t <title>, --title=<html-title>
            Option required for HTML format. Represents the title of the page.
        -o <output-file-format>, --output=<output-file-format>
            Output file format. If it is not specified, or an invalid format is used, HTML is assumed.
            Valid formats: docx, pdf, txt
        -h, --help
            Prints this help manual.
        -l, --license:
            Prints application license.
        -v, --version:
            Prints application version
    """
    VERSION_INFO = """
MdConv version {}
Newer versions @ Github https://github.com/AndersonPaschoalon/Md2Html

Created by Anderson Paschoalon: <anderson.paschoalon@gmail.com>
    """

    @staticmethod
    def _conv_html_temp(md_file: str, title=""):
        """
        Creates a temporary HTML version of the original md file. Returns the name of the created file.
        :param md_file: path to the md file.
        :param title: title of the html file
        :return: random name of the created file.
        """
        html_file = ""
        temp_sufix = "_temp_" + ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        try:
            html_file = os.path.splitext(md_file)[0] + temp_sufix + ".html"
            if exists(md_file):
                file = open(md_file, mode='r')
                md_str = file.read()
                file.close()
                Md.html_file(md_str, html_file, title)
            else:
                print("**Error: File <" + md_file + "> could not be found or do not exit.")
                sys.exit(Main.RET_ERROR_FILE_NOT_FOUND)
        except:
            print("**Error: Exception caught while processing files.")
            traceback.print_exc()
            sys.exit(Main.RET_ERROR_EXCEPTION_PROCESSING_FILES)
        return html_file

    @staticmethod
    def help_menu():
        print(Main.APP_MANPAGE)
        print("")

    @staticmethod
    def print_version():
        print(str(Main.VERSION_INFO).format(Main.APP_VERSION))
        print("")

    @staticmethod
    def print_license():
        print(Main.LICENSE)

    @staticmethod
    def convert_html(md_file: str, title=""):
        try:
            html_file = os.path.splitext(md_file)[0] + ".html"
            if exists(md_file):
                file = open(md_file, mode='r')
                md_str = file.read()
                file.close()
                Md.html_file(md_str, html_file, title)
            else:
                print("**Error: File <" + md_file + "> could not be found or do not exit.")
                sys.exit(Main.RET_ERROR_FILE_NOT_FOUND)
        except:
            print("**Error: Exception caught while processing files.")
            traceback.print_exc()
            sys.exit(Main.RET_ERROR_EXCEPTION_PROCESSING_FILES)

    @staticmethod
    def convert_docx(md_file: str):
        temp_html = ""
        try:
            docx_file = os.path.splitext(md_file)[0]
            if exists(md_file):
                temp_html = Main._conv_html_temp(md_file=md_file, title="")
                new_parser = HtmlToDocx()
                new_parser.parse_html_file(temp_html, docx_file)
                time.sleep(0.1)
                os.remove(temp_html)
            else:
                print("**Error: File <" + md_file + "> could not be found or do not exit.")
                sys.exit(Main.RET_ERROR_FILE_NOT_FOUND)
        except:
            print("**Error: Exception caught while processing files.")
            traceback.print_exc()
            if exists(temp_html):
                os.remove(temp_html)
            sys.exit(Main.RET_ERROR_EXCEPTION_PROCESSING_FILES)

    @staticmethod
    def convert_pdf(md_file: str):
        temp_html = ""
        try:
            pdf_file = os.path.splitext(md_file)[0] + ".pdf"
            if exists(md_file):
                temp_html = Main._conv_html_temp(md_file=md_file, title="")
                options = {'page-size': 'A4',
                           'dpi': 400,
                           'encoding': 'utf-8',
                           'margin-top': '2cm',
                           'margin-bottom': '2cm',
                           'margin-left': '3cm',
                           'margin-right': '1cm'
                           }
                pdfkit.from_file(temp_html, pdf_file, options=options)
                time.sleep(0.1)
                os.remove(temp_html)
            else:
                print("**Error: File <" + md_file + "> could not be found or do not exit.")
                sys.exit(Main.RET_ERROR_FILE_NOT_FOUND)
        except:
            print("**Error: Exception caught while processing files.")
            traceback.print_exc()
            if exists(temp_html):
                os.remove(temp_html)
            sys.exit(Main.RET_ERROR_EXCEPTION_PROCESSING_FILES)

    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    @staticmethod
    def main(argv):
        md_file = ''
        title = ''
        out_fmt = ''
        try:
            opts, args = getopt.getopt(argv,"m:t:o:hvl", ["md=", "title=", "output=", "help", "version", "license"])
        except getopt.GetoptError:
            print("**Error parsing arguments.")
            traceback.print_exc()
            sys.exit(Main.RET_ERROR_PARSING_ARGS)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Main.help_menu()
                return
            elif opt in ("--md", "-m"):
                md_file = arg
            elif opt in ("-t", "--title"):
                title = arg
            elif opt in ("-o", "--output"):
                out_fmt = arg
            elif opt in ("-l", "--license"):
                Main.print_license()
                return
            elif opt in ("-v", "--version"):
                Main.print_version()
                return
        if md_file != "":
            out_fmt = str(out_fmt).lower()
            if out_fmt == "html":
                Main.convert_html(md_file, title)
            elif out_fmt == "docx":
                Main.convert_docx(md_file)
            elif out_fmt == "pdf":
                Main.convert_pdf(md_file)
            elif out_fmt == "":
                print("Note: using default output format HTML.")
                Main.convert_html(md_file, title)
            else:
                print("**Error, Could not recognize output format {}.".format(out_fmt))
                sys.exit(Main.RET_INVALID_FORMAT)
            print("Markdown file {} converted to {} successfully!".format(md_file, out_fmt))
            return
        else:
            print("** Error, empty mandatory parameter --md.")
            Main.help_menu()
            sys.exit(Main.RET_ERROR_INVALID_ARGS)


if __name__ == "__main__":
    try:
        Main.main(sys.argv[1:])
    except:
        print("**Error: Exception in the application")
        traceback.print_exc()
        sys.exit(Main.RET_ERROR_GENERIC)

