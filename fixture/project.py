from selenium.webdriver.common.by import By
from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    project_cache = None

    def create_new_project(self, project):
        wd = self.app.wd
        self.manage_page()
        self.manage_projects()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        self.submit_project_creation()
        self.project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.manage_page()
            self.manage_projects()
            self.project_cache = []
            for element in wd.find_elements(By.XPATH, "//table[3]/*/tr[@class='row-1' or @class='row-2']"):
                cells = element.find_elements(By.TAG_NAME, "td")
                id = cells[0].find_element(By.TAG_NAME, "a").get_attribute("href").split("=")[-1]
                name = cells[0].text
                self.project_cache.append(Project(id=id, name=name))
        return list(self.project_cache)

    def delete_project(self, id):
        wd = self.app.wd
        self.manage_page()
        self.manage_projects()
        self.select_project(id)
        self.delete_button()
        self.confirm_deletion()
        self.project_cache = None

    def submit_project_creation(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def manage_projects(self):
        wd = self.app.wd
        wd.get(self.app.base_url + "/manage_proj_page.php")

    def manage_page(self):
        wd = self.app.wd
        wd.get(self.app.base_url + "/manage_overview_page.php")
    def select_project(self, id):
        wd = self.app.wd
        wd.find_element(By.XPATH, f"//a[@href='manage_proj_edit_page.php?project_id={id}']").click()

    def delete_button(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

    def confirm_deletion(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
