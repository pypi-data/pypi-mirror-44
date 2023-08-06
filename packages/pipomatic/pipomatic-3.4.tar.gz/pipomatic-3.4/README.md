# Pipomatic

Automatically create pip installable modules from functions in your Jupyter notebook

When I'm working on a data science or a [Papermill](https://github.com/nteract/papermill) automation project, I will often write a function in a Jupyter notebook cell and, once it's doing what I want it to do, I'll pull it out into a Python file and import it as a module.

This helps keep my notebooks clean and code DRYer.

But I find it a bit inconvenient to work in multiple environments and to set up different ways of testing code. And when I'm working for a different client I have to copy or rewrite the code to run in their environment.

With Pipomatic, when I have a function I want to keep, I put it into a Jupyter notebook, add the data I need to ensure it generates the right outputs, and run Pipomatic to push the functions in the notebook to pip where I can just pip install them anywhere.

## Install

    pip install pipomatic

## Using pipomatic

Once you have installed pipomatic, the next step is to convert your notebook. 

### Step 1: Create a notebook with your functions you want to put on pip

The image below shows a sample notebook called _my_pipomatic_func_. Any cells tagged as 'test' are not sent to pip. So in the notebook below, the only cells sent to pip are the markdown cell and the _square_it_ function. None of the output content is sent to pip.

> Note that your notebook name must not match an existing module name in pip. An easy way to do this is to preface your notebook name with your PyPI username. For example, my PyPI username is eq8r so I would name the notebook eq8r_my_pipomatic_func

The reason pipomatic excludes the cells tagged as _test_ and the output cells is so that you can run your notebook with test data and confirm the output is what you expect without this information being made public in pip.

![Notebook](./sample_notebook/cells_tagged_test.png)

### Step 2: Run pipomatic on your notebook

Running `pipomatic my_pipomatic_func` in a terminal window like you used to launch your Jupyter notebook creates a python file and submits it to pip so the functions in the notebook can be pip installed.

This creates a python file called _my_pipomatic_func.py_ that contains the code and another file called setup.py that tells pip where to store the file.

> When you run pipomatic, you will be asked to provide your PyPI username and password to upload the code to your PyPI project workspace. If you have not yet registered at PyPI.org, you can do so here: https://pypi.org/account/register/

The image below shows the code that is uploaded to pip. You can see that the cells that are tagged _text_ are excluded, the output from running the cells is excluded and the markup cells containing headers and explanatory text are included as comments.

![Python file](./sample_notebook/python_file.png)

When you log into PyPI, you will see your project at the top of your project list.

![PyPI Project](./sample_notebook/pypi_project.png)

### Step 3: pip install your module anywhere

You can now `pip install my_pipomatic_func` to install _my_pipomatic_func_ anywhere!

For example, in your Jupyter notebooks, you could do this:

    import my_pipomatic_func as sq
    sq.square_it(4)
    
Which returns the result _16_.

![Using the function in a notebook](./sample_notebook/trying_it_out.png)

## To do

The code is slapdash and there's hardly any tests.

There's lots of different directions this project can go. It currently caters for a single workflow but I can imagine lots of possible variations on it.

For example, in addition to pushing it to PyPI, I would find it useful to create a module that I can dynamically import into my current Jupyter notebooks so I don't have to `pip install --upgrade` every time I update the code in my pip module.

I also sometimes forget to mark test cells as 'test' which means the module fails when it gets converted from a notebook file to a python file or it fails once it is on PyPI. I could see several different ways of tackling this problem such as only pushing functions and classes to PyPI or, at least, running the notebook and validating the output before pushing it to PyPI.

But it's at a stage where I am keen to see how this fits into your data science and automation workflows.

I hope you find it useful. Please message me at doug.hudgeon@eq8r.com with your feedback.
