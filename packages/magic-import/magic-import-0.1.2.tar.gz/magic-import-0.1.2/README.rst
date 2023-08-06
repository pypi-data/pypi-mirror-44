magic-import
============


Import python object from string and return the reference of the object.
The object can be a class, instance, variable and anything else,
and can be from class, instance, module, global/local environment.


Install
-------

::

    pip install magic-import


Usage
-----

::

    from magic_select import import_from_string
    listdir = import_from_string("os.listdir")
    files = listdir(".")

