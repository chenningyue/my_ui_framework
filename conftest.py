import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    pg = browser.new_page()
    yield pg
    pg.close()

@pytest.fixture(autouse=True)
def screenshot_on_failure(request,page):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"report/{request.node.name}.png",full_page=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item,"rep_" + rep.when,rep)