from suds.client import Client
from suds import WebFault
from model.project_form import ProjectForm


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, base_url, username, password):
        api_page_url = "{}/api/soap/mantisconnect.php?wsdl".format(base_url)
        client = Client(api_page_url)
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, base_url, username, password):
        projects_list = []
        api_page_url = "{}/api/soap/mantisconnect.php?wsdl".format(base_url)
        client = Client(api_page_url)
        projects = client.service.mc_projects_get_user_accessible(username, password)
        for project in projects:
            projects_list.append(ProjectForm(project_name=project.project_name))
        return list(projects_list)
        # try:
        #     projects = client.service.mc_projects_get_user_accessible(username, password)
        #     for project in projects:
        #         projects_list.append(ProjectForm(project_name=project.project_name))
        #     return list(projects_list)
        # except WebFault:
        #     return False

