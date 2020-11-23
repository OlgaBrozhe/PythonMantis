import re


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector("input[type='submit']").click()
        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)
        wd.get(url)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").click()
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector("input[value='Update User']").click()

    def extract_confirmation_url(self, text):
        # Search for string in mail body (text) starting with http and till the end of the string,
        # like http://localhost/mantisbt-1.2.20/verify.php?id=9&confirm_hash=98dc564d15154fd12764d272bba6ba76
        # group(0) - everything suitable for the request
        return re.search("http://.*$", text, re.MULTILINE).group(0)
