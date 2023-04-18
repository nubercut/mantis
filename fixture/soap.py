from suds.client import Client
from suds import WebFault
from model.project import Project
class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        username = self.app.config["webadmin"]["username"]
        password = self.app.config["webadmin"]["password"]
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        try:
            projects_list = self.convert_projects_to_model(list(client.service.mc_projects_get_user_accessible(username, password)))
            return projects_list
        except WebFault:
            return False

    def convert_projects_to_model(self, projects_list):
        def convert(project):
            return Project(id=str(project.id), name=project.name)
        return list(map(convert, projects_list))
