=====
Usage
=====

To use wrappedbrowser in a project::

    from wrappedbrowser import wrappedbrowser


To open a URL with the default browser::

    wrappedbrowser.open("https://www.example.com/")


To open a list of URL-s::

    wrappedbrowser.open([
        "https://www.example.com/",
        "https://www.python.org/",
    ])

If your browser supports `open_new` and `open_new_tab`, all url-s get openend in a common, new window.

To use a custom browser::

    wrappedbrowser.open("https://www.example.com/","chromium-browser")

For a list of available browser types, see the `documentation of the webbrowser standard library module <https://docs.python.org/3/library/webbrowser.html>`_
