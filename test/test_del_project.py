from model.project_form import ProjectForm
import random


def test_del_project(app, config):
    user_config = config['webadmin']['username']
    password_config = config['webadmin']['password']
    old_projects_list = app.soap.get_projects_list(app.base_url, user_config, password_config)
    if not old_projects_list:
        app.project.add_new_project(ProjectForm(project_name="TestProject",
                                                project_description="Test Project Description"))
        old_projects_list = app.soap.get_projects_list(app.base_url, user_config, password_config)
    project = random.choice(old_projects_list)
    app.project.del_project(project)
    new_projects_list = app.soap.get_projects_list(app.base_url, user_config, password_config)
    # Checks
    assert len(old_projects_list) - 1 == len(new_projects_list)
    old_projects_list.remove(project)
    sorted_old_projects_list = sorted(old_projects_list, key=(lambda x: x.project_name))
    sorted_new_projects_list = sorted(new_projects_list, key=(lambda x: x.project_name))
    assert sorted_old_projects_list == sorted_new_projects_list
