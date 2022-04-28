import markdown
import os
import traceback
import sys
import getopt
from os.path import exists


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

    @staticmethod
    def help_menu():
        print("Converts a markdown file to html.")
        print("")
        print("Usage:")
        print("\tmd2html --md <markdown-file> --title <html-title>")
        print("")
        print("Options:")
        print("\t--md|-m <markdown-file>: path to markdown file")
        print("\t--title|-t <html-title>: title to the HTML page title")
        print("\t--help|-h : prints this help manual")
        print("\t--license:l: prints application license")
        print("\t--version:v: prints application version")
        print("")

    @staticmethod
    def print_version():
        print("Md2Html version " + Main.APP_VERSION)
        print("Newer versions @ Github https://github.com/AndersonPaschoalon/Md2Html" + Main.APP_VERSION)
        print("")
        print("Created by Anderson Paschoalon: <anderson.paschoalon@gmail.com>")
        print("")

    @staticmethod
    def print_license():
        print(Main.LICENSE)

    @staticmethod
    def convert(md_file: str, title=""):
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

    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    @staticmethod
    def main(argv):
        md_file = ''
        title = ''
        ret_val = False
        try:
            opts, args = getopt.getopt(argv,"m:t:h:v:l",["md=","title=","help", "version", "license"])
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
            elif opt in ("-l", "--license"):
                Main.print_license()
                return
            elif opt in ("-v", "--version"):
                Main.print_version()
                return
        if md_file != "":
            Main.convert(md_file, title)
            print("Markdown file " + md_file + " converted to HTML successfully.")
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

