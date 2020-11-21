def test_add_project(app, json_data_projects):
    old_projects_list = app.project.get_projects_list()
    project = json_data_projects
    project.project_name = project.project_name.strip()
    if project not in old_projects_list:
        app.project.add_new_project(project)
        new_projects_list = app.project.get_projects_list()
        assert len(old_projects_list)+1 == len(new_projects_list)
        old_projects_list.append(project)
        assert sorted(old_projects_list, key=(lambda x: x.project_name)) == \
               sorted(new_projects_list, key=(lambda x: x.project_name))
