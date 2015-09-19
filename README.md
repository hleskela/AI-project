 The AI project
================
Team members:
-------------
   * Sarah Berenji
   * Andreas Forstén
   * Hannes Leskelä
   * Josefine Letzner

Project goal:
-------------
To implement a text analyser that, although on a basic level, correctly analyses and cathegorizes text.a
The lowest grade that we will aim for is C, but due to limited time and resouces we won't aim for an A from the start. If the project work load is easier than expected, then the target grade might change to a higer one.
For information regarding the requirements for each grade, please see this page: [project topics](https://www.kth.se/social/course/DD2380/subgroup/ht-2015-ai15/page/topics-4/)

Tools:
------
We are going to use Python >= 3.0 to write the text analyser.
Tools will be added as the project goes along.

Setting up the work environment:
--------------------------------

### Installing the necessities:
Start by making sure that you've got a working python3 installation on your system:

   $ python3 --version
   Python 3.4.0

If the output isn't something in the likes of the above then make sure that you install a working version on your system.
Next, I highly suggest that you install virtualenv so that you can work in a special virtual environment for this project. This is made easiest with 'pip'. First check and see if you have pip3:

      $ pip3 --version
      pip 1.5.4 from /usr/lib/python3/dist-packages (python 3.4)

If you don't, "sudo apt-get install python3-pip" will do the trick. After that, you can install virtualenv with pip as such:

   $ sudo pip3 install virtualenv

### Setting up a virtual environment:

After you've installed virtualenv, setting up a virtual environment called "venv" is as easy as such:

   $ virtualenv -p /usr/bin/python3 venv

I highly suggest that you call your virtual environment "venv" since this folder name will already be ignored by git (see the .gitignore)
To activate the virtual environment, simply issue:

   $ source venv/bin/activate

Now your prompt will look something like this:

   (venv)hannes@hannes-1225B:~/Documents/AI_project$

indicating that you are now working in a virtual environment. So from now on, everything you install with pip for the project will be placed in the venv folder, thus not cluttering your main python installation with different packages. Just issue:

   (venv)$ pip3 install <package-name>

and it will be installed. To deactivate the virtual environment, simply issue:

   (venv)$ deactivate

and your prompt will return to normal. If you issue any "pip install" commands, they will now be placed in your systems python directories as usual. 

### Checking code quality with pylint

pylint can be installed in your virtual environment with:

   (venv)$ pip install pylint

we also recommend using pre-commit hooks to automatically check your code with pylint. To initiate the pre-commit hook you can link it to the .git/hooks directory. Simply do:

'ln -s /full/path/to/the/git/root/directory/Scripts/pylint_test_suite.py /full/path/to/the/git/root/directory/.git/hooks/pre-commit'


### Quick setup of the packages required in the virtual environment:

Issuing the following command after setting up the virtual environment will download all the packages that is necessary for running the project:

   $ pip install -r requirements.txt