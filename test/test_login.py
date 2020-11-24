def test_login(app, config):
    username = config['webadmin']['username']
    password = config['webadmin']['password']
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)