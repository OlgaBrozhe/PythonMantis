# -*- coding: utf-8 -*-
from fixture.application import Application
import pytest
import json
import os.path


fixture = None
cfg_target = None


# Load configuration file
def load_config(file):
    global cfg_target
    if cfg_target is None:
        # Get the path, where the file is located - dirname. Join the directory path with the file path
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file_to_use:
            cfg_target = json.load(file_to_use)
    return cfg_target


# Load web configuration from the configuration file
@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--cfg_target"))["web"]
    webadmin_config = load_config(request.config.getoption("--cfg_target"))["webadmin"]
    # Create fixture 1. if it is not initialised or 2. if it is initialised but invalid, e.g. browser failed
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
    fixture.session.ensure_login(username=webadmin_config["username"], password=webadmin_config["password"])
    return fixture


# Destroy/stop the fixture
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        # Logout, if not currently logged out
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


# Parse test run options
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--cfg_target", action="store", default="cfg_target.json")