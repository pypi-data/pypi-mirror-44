# pyquilted

Generate Quilted™ resumes from Yaml in python. Find out more about [Quilted](https://github.com/cocoroutine/quilted)

`$ pip install pyquilted`




## Requirements

Pyquilted uses [Wkhtmltopdf](https://wkhtmltopdf.org/) to convert html to pdf via [python-pdfkit](https://github.com/JazzCore/python-pdfkit).


#### Install wkhtmltopdf


Debian/Ubuntu

`$ sudo apt-get install wkhtmltopdf`


MacOs HomeBrew

`$ brew install caskroom/cask/wkhtmltopdf`


Windows and other platforms:

[link to wkhtmltopdf binaries](https://wkhtmltopdf.org/downloads.html)




## Sample

Generate a sample yaml file so that you can use it as a template for your resume

`$ pyquilted --sample mysample.yml`




## Pdf

Convert your yaml file to a quilted resume pdf

`$ pyquilted --pdf mysample.yml myresume.pdf`




## Custom Formatting

```bash

style: css styles to apply to resume content

--color         "color|#rgb"    css color code for your name
--font          "font"          css font for resume content
--font-other    "font"          css font override for heading/contacts
--font-size     "size"          css font size for resume content

```



## Html

If you prefer to customize the html and then print using your browser

`$ pyquilted --html mysample.yml myresume.html`

