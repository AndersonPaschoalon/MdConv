import time
import os
import re
import traceback
import sys
import getopt
from os.path import exists
from htmldocx import HtmlToDocx
import random
from xhtml2pdf import pisa
from gazpacho import Soup
from Md import Md
from Cd import cd

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
            Valid formats: html, docx, pdf, txt
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
    def _convert_html_to_plaintext(source_html, output_filename):
        text = Soup(source_html).strip(whitespace=False)  # to keep "\n" characters intact
        text = text.strip()
        text = re.sub(r'\n\n\n(\n)*', "\n\n", text, flags=re.S)
        print(text)
        with open(output_filename, "w") as txt_file:
            txt_file.write(text)

    @staticmethod
    def _convert_html_to_pdf(source_html, output_filename):
        # open output file for writing (truncated binary)
        result_file = open(output_filename, "w+b")

        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            source_html,  # the HTML to convert
            dest=result_file)  # file handle to recieve result

        # close output file
        result_file.close()  # close output file

        # return False on success and True on errors
        return pisa_status.err

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
            if exists(md_file):
                docx_file = os.path.splitext(md_file)[0]
                dir_name = os.path.dirname(md_file)
                with cd(dir_name):
                    md_in = os.path.basename(md_file)
                    docx_out = os.path.basename(docx_file)
                    temp_html = Main._conv_html_temp(md_file=md_in, title="temp htmp")
                    new_parser = HtmlToDocx()
                    new_parser.parse_html_file(temp_html, docx_out)
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
                md_in = os.path.basename(md_file)
                dir_name = os.path.dirname(md_file)
                pdf_out = os.path.basename(pdf_file)
                with cd(dir_name):
                    md_str = ""
                    with open(md_in) as file:
                        md_str = file.read()
                    html_str = Md.html_str(md=md_str, title="Temp HTML String")
                    Main._convert_html_to_pdf(source_html=html_str, output_filename=pdf_out)
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
    def convert_txt(md_file: str):
        temp_html = ""
        try:
            txt_file = os.path.splitext(md_file)[0] + ".txt"
            if exists(md_file):
                md_in = os.path.basename(md_file)
                dir_name = os.path.dirname(md_file)
                txt_out = os.path.basename(txt_file)
                with cd(dir_name):
                    md_str = ""
                    with open(md_in) as file:
                        md_str = file.read()
                    html_str = Md.html_str(md=md_str, title="Temp HTML String")
                    html_str = re.sub(r"<script>.*</script>", "", html_str, flags=re.S)
                    html_str = re.sub(r"<style>.*</style>", "", html_str, flags=re.S)
                    html_str = re.sub(r"<head>.*</head>", "", html_str, flags=re.S)
                    Main._convert_html_to_plaintext(source_html=html_str, output_filename=txt_out)
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
            elif out_fmt == "txt":
                Main.convert_txt(md_file)
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

