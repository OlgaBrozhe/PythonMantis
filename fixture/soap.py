from suds.client import Client
from suds import WebFault
from model.project_form import ProjectForm


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        projects_list = []
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        projects = list(client.service.mc_projects_get_user_accessible(username, password))
        for project in projects:
            projects_list.append(ProjectForm(project_name=project.project_name))
        return list(projects_list)
