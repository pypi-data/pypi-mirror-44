# -*- coding: utf-8 -*-

"""Main module."""

import webbrowser

from wrappedbrowser.errors import InvalidDestinationError


def open(destination, browser_type=None):
    """Opens a single url or a list of urls.

    ``destination``:
        If it's a string, it's opened if possible in a new window.
        If it's a list, all url-s are opened.

    ``browser_type``:
        Optional.
        If provided, it's passed to the `webbrowser.get` function.
    """
    browser = _get_browser(browser_type)
    if isinstance(destination, str):
        browser.open_new(destination)
        return
    if isinstance(destination, list):
        _open_multiple(destination, browser)
        return
    raise InvalidDestinationError


def _open_multiple(urls, browser):
    browser.open_new(urls[0])
    if len(urls) > 1:
        for u in urls[1:]:
            browser.open_new_tab(u)


def _get_browser(btype):
    if btype is None:
        return webbrowser.get()
    return webbrowser.get(btype)
