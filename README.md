![MdConv](./resources/markdown_here_med.png)
# MdConv

Just a simple command line app to convert Markdown files into different formats.
* HTML
* DOCX
* PDF
* TXT

If you type `mdconv.exe --help` you can read its usage manual:

```
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
```

In the script `tests\run-tests.py` there is a python scripts some examples. of usage can be found.

## Development and Build

* PyCharm Community was used for the development.
* To *build* the executable file and exeute the tests, just execute `.\build-app.bat`. The binary file will be located at `.\dist\`


## RELEASE HISTORY

2022.04.25, v0.1.0.0, First stable version

## Credits

* Application developed by Anderson Paschoalon

* Python packages used can be found at [requirements.txt](requirements.txt)

* App icon downloaded at https://icon-icons.com/pt/icone/markdown-aqui-logo/169967



## Changelog

2022.04.27, rc-v0.1.1.0, fixes on command line, display version




