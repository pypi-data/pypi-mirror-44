Introduction
============

The pyempt package is a python emacs package for type checking and other
syntax analysis. It is basically a simple wrapper around other python
syntax checkers to simplify the process of calling pylint, pep8, etc.
from something like emacs flymake.

In principle, you could do all of this with a a few `simple
scripts <http://stackoverflow.com/questions/1259873/how-can-i-use-emacs-flymake-mode-for-python-with-pyflakes-and-pylint-checking-co>`__.
It's nice being able to ``pip install`` something that works and
collaborate on improvements, however, and that is what pyempt is for.

Installation
============

To install pyempt, first do something like ``pip install pyempt`` or
``sudo pip install pyempt``. Then add something like the following to
your ``~/.emacs`` file to run pyempt.

::

    (when (load "flymake" t)
      (defun flymake-pyempt-init ()
        (let* ((temp-file (flymake-init-create-temp-buffer-copy
                   'flymake-create-temp-inplace))
           (local-file (file-relative-name
                temp-file
                (file-name-directory buffer-file-name))))
          (list "pyempt"  (list local-file))))
       (add-to-list 'flymake-allowed-file-name-masks
                 '("\\.py\\'" flymake-pyempt-init)))

    (add-to-list 'flymake-allowed-file-name-masks
      '("\\.py\\'" flymake-pyempt-init))

    ;; Uncomment following line if you want flymake to start on file load
    ;;(add-hook 'find-file-hook 'flymake-find-file-hook)

After you restart emacs or reload your init file, flymake should
automatically start and call pyempt.

Usage
=====

If you have installed pyempt and setup emacs to use it in flymake, there
isn't anything you need to do to use pyempt. Instead, it will run
automatically inside emacs.

If you want to run it from the command line, you can type

::

    pyempt --help

to see options and usage instructions or type

::

    pyempt <PATH_TO_CHECK>

to run checks on everything in a given path.

Since pyempt will return a non-zero exit code if any of its checkers
returns a non-zero code, you can simply check the return value of pyempt
in build scripts or continuous integration tools.

Troubleshooting
===============

If you have problems, the first thing to do is to try and run pyempt
manually via something like

::

    pyempt <FILE_TO_CHECK>

You can turn on logging via

::

    pyempt <FILE_TO_CHECK> --log_level 0

You can get further help on the command line program via

::

    pyempt --help

Forking
=======

If you want to fork pyempt, you may find the following useful:

1. The ``README.md`` file is the main file. Generate the rst version via
   something like ``pandoc README.md -t rst > README.rst``
2. Upload to pypi via something like ``make pypi`` provided you have
   your ``~/.pypirc`` setup correctly.
