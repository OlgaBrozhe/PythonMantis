def test_add_project(app, config, json_data_projects):
    user_config = config['webadmin']['username']
    password_config = config['webadmin']['password']
    old_projects_list = app.soap.get_projects_list(app.base_url, user_config, password_config)
    project = json_data_projects
    project.project_name = project.project_name.strip()
    if project not in old_projects_list:
        app.project.add_new_project(project)
        new_projects_list = app.soap.get_projects_list(app.base_url, user_config, password_config)
        assert len(old_projects_list)+1 == len(new_projects_list)
        old_projects_list.append(project)
        sorted_old_projects_list = sorted(old_projects_list, key=(lambda x: x.project_name))
        sorted_new_projects_list = sorted(new_projects_list, key=(lambda x: x.project_name))
        assert sorted_old_projects_list == sorted_new_projects_list

