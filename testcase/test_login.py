import pytest

from pages.login_page import LoginPage
from data.test_data import username, password,expected,expected_empty
from playwright.sync_api import expect


def test_login_success(page):
    lp = LoginPage(page)
    lp.goto_login_page()
    lp.login(username,password)
    expect(lp.result).to_contain_text(expected)

def test_login_null(page):
    lp = LoginPage(page)
    lp.goto_login_page()
    lp.login(username,"")
    expect(lp.result).to_contain_text(expected_empty)