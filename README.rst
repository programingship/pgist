pgist
=====

A Python command-line wrapper with github3.py library to access GitHub Gist.

Installation
------------
You can install with `pip`:

::

    pip install pgist --upgrade

Or with `easy_install`:

::

    easy_install -U pgist

Command
-------
To upload the contents of `a.py` just:

::

    pgist a.py

Upload multiple files:

::

    pgist a b c

Use `-p` to make the gist private:

::

    pgist a.py -p

Use `-d` to add a description:

::

    pgist -d "Say something" a.py

You can update existing gists with `-u`:

::

    pgist b.py c.py -u 2c93e03266634cd6e273

List your public gists:

::

    pgist -l

And list all contains private ones:

::

    pgist -l -A

See `pgist --help` for more detail.

Login
-----
If you want to associate your gists with your GitHub account, you need to login
with pgist. It doesn't store your username and password, it just uses them to get
an OAuth2 token (with the "gist" permission).

::

    pgist --login
    GitHub username(default is xxxxx): douglarek
    GitHub password for douglarek:
    Done ...

After you've done this, you can still upload gists anonymously with `-a`:

::

    pgist a.py -a

Thanks
------
* github3.py_ by Ian Cordasco.

License
-------
Licensed under the Apache 2.0 license. `Bug-reports, and pull requests`_ are welcome.

.. _github3.py: https://github.com/sigmavirus24/github3.py
.. _`Bug-reports, and pull requests`: https://github.com/douglarek/pgist
