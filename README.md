Djembe
======

Djembe is a toy Django environment for learning the template syntax. As an added bonus, it also
contains Jinja template support via the Coffin library, so you can mix-and-match your learning.

Note
----

Djembe differs significantly from normal Django applications in structure, for simplicity's sake.
This, however, should not be a problem for template language learning (which is what it's for).

First time usage
----------------

When you spin up Djembe for the first time, you'll want to set up a `virtualenv` for it before
installing Djembe's package requirements.

For Ubuntu/Debian Linux environments, if you are currently in the Djembe directory, the following
should do. For other environments, look for tutorials on the web.

```
sudo apt-get install python-virtualenv python-pip
virtualenv --system-site-packages djembe_virtualenv
. djembe_virtualenv/bin/activate
pip install -r requirements.txt
```

Usage
-----

When you've done the above installation, the following should do to start the Django development
server with Djembe. (If you are following up from the First Time Usage bit above, you don't
need to do the `activate` part. But it doesn't hurt, either.)

```
. djembe_virtualenv/bin/activate
python djembe.py runserver 0.0.0.0:8000
```

Now, if you visit http://localhost:8000/, you should be greeted by Djembe's index page, which has
more useful information.

Good luck!
----------