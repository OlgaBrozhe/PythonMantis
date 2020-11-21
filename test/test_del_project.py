from model.project_form import ProjectForm
import random


def test_del_project(app):
    old_projects_list = app.project.get_projects_list()
    if not old_projects_list:
        app.project.add_new_project(ProjectForm(project_name="TestProject",
                                                project_description="Test Project Description"))
        old_projects_list = app.project.get_projects_list()
    project = random.choice(old_projects_list)
    app.project.del_project(project)
    new_projects_list = app.project.get_projects_list()
    # Checks
    assert len(old_projects_list) - 1 == len(new_projects_list)
    old_projects_list.remove(project)
    assert sorted(old_projects_list, key=(lambda x: x.project_name)) == \
           sorted(new_projects_list, key=(lambda x: x.project_name))