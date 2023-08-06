#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wrappedbrowser` package."""

import webbrowser
from unittest.mock import MagicMock

import pytest

from wrappedbrowser import wrappedbrowser
from wrappedbrowser.errors import InvalidDestinationError


def test_with_browser_type(mocker):
    """Test with an explicit browser type."""
    mocker.patch.object(webbrowser, "get")

    wrappedbrowser.open("https://www.example.com", "chromium-browser")

    webbrowser.get.assert_called_once_with("chromium-browser")


def test_open_one_url(mocker):
    """Test with a single url."""
    mocked_browser = MagicMock()
    mocker.patch.object(webbrowser, "get", return_value=mocked_browser)
    mocker.patch.object(mocked_browser, "open_new")

    wrappedbrowser.open("https://www.example.com")

    webbrowser.get.assert_called_once()
    mocked_browser.open_new.assert_called_once_with("https://www.example.com")


def test_open_two_urls(mocker):
    """Test with a list of urls."""
    mocked_browser = MagicMock()
    mocker.patch.object(webbrowser, "get", return_value=mocked_browser)
    mocker.patch.object(mocked_browser, "open_new")

    wrappedbrowser.open(["https://www.example.com", "https://www.python.org"])

    webbrowser.get.assert_called_once()
    mocked_browser.open_new.assert_called_once_with("https://www.example.com")
    mocked_browser.open_new_tab.assert_called_once_with("https://www.python.org")


def test_invalid_destination():
    with pytest.raises(InvalidDestinationError):
        wrappedbrowser.open(5)
