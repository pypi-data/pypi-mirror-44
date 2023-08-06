.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ericmjl/pyjanitor/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Implementing a feature generally means writing a function that has the
following form:

.. code-block:: python

    @pf.register_dataframe_method
    def function(df, *args, **kwargs):
        # stuff done here
        return df

The function signature should take a pandas dataframe as the input, and return
a pandas dataframe as the output. Any manipulation to the dataframe should be
implemented inside the function.

This function should be implemented in `functions.py`, and should have a test
accompanying it in `tests/functions/test_<function_name_here>.py`.

When writing a test, the minimum acceptable test is an "example-based test".
Under ``janitor.testing_utils.fixtures``, you will find a suite of example
dataframes that can be imported and used in the test.

If you are more experienced with testing, you can use Hypothesis to
automatically generate example dataframes. We provide a number of
dataframe-generating strategies in ``janitor.testing_utils.strategies``.

If you're wondering why we don't have to implement the method chaining
portion, it's because we use pandas-flavor's `register_dataframe_method`,
which registers the function as a pandas dataframe method.

Write Documentation
~~~~~~~~~~~~~~~~~~~

``pyjanitor`` could always use more documentation, whether as part of the
official pyjanitor docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ericmjl/pyjanitor/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `pyjanitor` for local development.

1. Fork the `pyjanitor` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pyjanitor.git

3. Install your local copy into a conda environment. Assuming you have conda installed, this is how you set up your fork for local development::

    $ cd pyjanitor/
    $ conda env create -f environment-dev.yml
    $ python setup.py develop

4. Create a branch for local development::

New features added to pyjanitor should be done in a new branch you have based off of the latest version of the `dev` branch. The protocol for pyjanitor branches for new development is that the `master` branch mirrors the current version of pyjanitor on PyPI, whereas `dev` branch is for additional features for an eventual new official version of the package which might be deemed slightly less stable. Once more confident in the reliability / suitability for introducing a batch of changes into the official version, the `dev` branch is then merged into `master` and the PyPI package is subsequently updated.

To base a branch directly off of `dev` instead of `master`, create a new one as follows:

    $ git checkout -b name-of-your-bugfix-or-feature dev

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests::

    $ flake8 janitor tests
    $ py.test

   flake8 and pytest are instaled when you create the development environment.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website where when you are picking out which branch to merge into, you select `dev` instead of `master`.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.

Tips
----

To run a subset of tests::

    $ py.test tests.test_functions
