# SmartyDoc

SmartyDoc provides an easy-to-use pipeline helping Jupyter users to create
gorgeous PDF documents, especially for data analytics field.
It provides convenient tools to convert **Jupyter Notebook** `ipynb` file into
a HTML page with 'standard' structure, thus the users could render the page with
customized css file, and further export to PDF format.

We also provide a Jupyter Notebook Extension named *printview2*, helping you
to create PDF document with few clicks.

The pipeline is based on various libraries, i.e. **WeasyPrint**, **Plotly**.

## Easy installation

Download SmartyDoc source code to <your_directory> by [clicking here](https://github.com/sealhuang/SmartyDoc/archive/master.zip) or executing ```$ git clone https://github.com/sealhuang/SmartyDoc <your_directory>```. Then:

```
$ cd <your directory>
$ python setup.py install
```

To install the Jupyter Notebook Extension *printview2*, you can copy the
printview2 directory into the Jupyter nbextensions directory.

## Note

* In ubuntu system, we can create a `.fonts` directory in the home, and put
new fonts in it which used in html and svg files.

* In order to create static images successfully using plotly, we should install
xvfb.
