from model.project import Project
import random


def test_del_project(app):
    app.session.ensure_login("administrator", "root")
    if len(app.project.get_project_list()) == 0:
        app.project.create_new_project(Project(name="Test"))
    old_projects = app.soap.get_project_list()
    projects = random.choice(old_projects)
    app.project.delete_project(projects.id)
    new_projects = app.soap.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(projects)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)