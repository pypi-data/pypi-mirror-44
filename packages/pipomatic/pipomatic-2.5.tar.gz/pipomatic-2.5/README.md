# Pipomatic

Automatically create pip installable modules from functions in your Jupyter notebook

When I'm working on a data science or a[Papermill](phttps://github.com/nteract/papermill) automation project, I will often write a function in a Jupyter notebook cell and, once it's doing what I want it to do, I'll pull it out into a Python file and import it as a module.

This helps keep my notebooks clean and code DRYer.

But I find it a bit inconvenient to work in multiple environments and to set up different ways of testing code. And when I'm working for a different client I have to copy or rewrite the code to run in their environment.

With Pipomatic, when I have a function I want to keep, I put it into a Jupyter notebook and run Pipomatic to push the functions in the notebook to pip where I can just pip install them anywhere.

## Install

    pip install pipomatic

## Using pipomatic

Once you have installed pipomatic, the next step is to convert your notebook. 

The image below shows a sample notebook called _my_pipomatic_func_. Any cells tagged as 'test' are not sent to pip. So in the notebook below, the only cells sent to pip are the markdown cell and the _square_it_ function. None of the output content is sent to pip.

The reason pipomatic excludes the cells tagged as _test_ and the output cells is so that you can run your notebook with test data and confirm the output is what you expect without this information being made public in pip.

![Notebook](./sample_notebook/cells_tagged_test.png)

Running `pipomatic my_pipomatic_func` in a terminal window like you used to launch your Jupyter notebook creates a python file and submits it to pip so the functions in the notebook can be pip installed.

