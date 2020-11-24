# -*- coding: utf-8 -*-
from fixture.application import Application
from gen import genereate
import pytest
import json
import jsonpickle
import os.path
import importlib
import ftputil


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


# Load data from the configuration file
@pytest.fixture(scope="session")
def config(request):
    config_request = request.config.getoption("--cfg_target")
    return load_config(config_request)


# Load web configuration from the configuration file
@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    # Create fixture 1. if it is not initialised or 2. if it is initialised but invalid, e.g. browser failed
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # Comment out the string below for run/debug test_login.py
    fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture


# FTP configuration
@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    # Restore FTP configuration
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        # Delete the backup file, if exists
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        # Rename the original file into backup file
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        # Upload test config file
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


# Destroy/stop the main fixture
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


# Load test data from JSON file
def pytest_generate_tests(metafunc):
    # To load test data - form fixture, use parameters with prefix "data_", but remove the prefix (first 5 symbols)
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture)
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            genereate()
            testdata = load_from_json(fixture[10:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.{}".format(module)).testdata


def load_from_json(file):
    file_target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/{}.json".format(file))
    with open(file_target) as file_in_use:
        return jsonpickle.decode(file_in_use.read())


