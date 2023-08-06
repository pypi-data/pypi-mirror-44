"""Helper general purpose functions"""
import importlib
import shutil
import json
import os
import uuid
import traceback
import glob
import re
from datetime import datetime
from distutils.version import StrictVersion

from golem.core import settings_manager
from golem.core import file_manager


def get_test_cases(workspace, project):
    path = os.path.join(workspace, 'projects', project, 'tests')
    test_cases = file_manager.generate_file_structure_dict(path)
    return test_cases


def get_pages(workspace, project):
    path = os.path.join(workspace, 'projects', project, 'pages')
    pages = file_manager.generate_file_structure_dict(path)
    return pages


def get_suites(workspace, project):
    path = os.path.join(workspace, 'projects', project, 'suites')
    suites = file_manager.generate_file_structure_dict(path)
    return suites


def get_projects(workspace):
    path = os.path.join(workspace, 'projects')
    projects = next(os.walk(path))[1]
    projects = [x for x in projects if x != '__pycache__']
    return projects


def project_exists(workspace, project):
    return project in get_projects(workspace)


def get_directory_tests(workspace, project, directory):
    """Return a list with all the test cases of a given directory"""
    path = os.path.join(workspace, 'projects', project, 'tests', directory)
    tests = file_manager.get_files_dot_path(path, extension='.py')
    if directory:
        dotpath = '.'.join(os.path.normpath(directory).split(os.sep))
        tests = ['.'.join([dotpath, x]) for x in tests]
    return tests


def get_timestamp():
    time_format = "%Y.%m.%d.%H.%M.%S.%f"
    timestamp = datetime.today().strftime(time_format)
    # remove last 3 decimal places from microseconds
    timestamp = timestamp[:-3]
    return timestamp


def get_date_from_timestamp(timestamp):
    date = datetime.strptime(timestamp, '%Y.%m.%d.%H.%M.%S.%f')
    return date


def display_tree_structure_command_line(structure, lvl=0):
    """Displays a directory tree structure to the command line"""
    for element in structure:
        if element['type'] == 'file':
            print('{}{}'.format(' ' * lvl * 2, element['name']))
        else:
            print('{}{}/'.format(' ' * lvl * 2, element['name']))
            display_tree_structure_command_line(element['sub_elements'], lvl + 1)


def separate_file_from_parents(full_filename):
    """Receives a full filename with parents (separated by dots)
    Returns a duple, first element is the filename and second element
    is the list of parents that might be empty"""
    splitted = full_filename.split('.')
    file = splitted.pop()
    parents = splitted
    return (file, parents)


def is_first_level_directory(workspace, project, directory):
    path = os.path.join(workspace, 'projects', project, 'tests', directory)
    return os.path.isdir(path)


def create_new_project(workspace, project):
    file_manager.create_directory(path_list=[workspace,'projects',project],
                                      add_init=True)
    # TODO, remove, don't create data folder for new projects
    # create_directory(path_list=[workspace, 'projects', project, 'data'], add_init=False)
    path_list = [workspace, 'projects', project, 'pages']
    file_manager.create_directory(path_list=path_list, add_init=True)
    path_list = [workspace, 'projects', project, 'reports']
    file_manager.create_directory(path_list=path_list, add_init=False)
    path_list = [workspace, 'projects', project, 'tests']
    file_manager.create_directory(path_list=path_list, add_init=True)
    path_list = [workspace, 'projects', project, 'suites']
    file_manager.create_directory(path_list=path_list, add_init=True)
    extend_path = os.path.join(workspace, 'projects', project, 'extend.py')
    open(extend_path, 'a').close()

    settings_manager.create_project_settings_file(workspace, project)

    for project_base_file in ('environments.json', 'secrets.json'):
        base_file_path = os.path.join(workspace, 'projects', project, project_base_file)
        with open(base_file_path, 'a') as base_file:
            base_file.write('{}')

    print('Project {} created'.format(project))


def create_test_dir(workspace):
    file_manager.create_directory(path_list=[workspace], add_init=True)
    file_manager.create_directory(path_list=[workspace, 'projects'],
                                  add_init=True)
    file_manager.create_directory(path_list=[workspace, 'drivers'],
                                  add_init=False)

    settings_manager.create_global_settings_file(workspace)

    users_path = os.path.join(workspace, 'users.json')
    open(users_path, 'a').close()
    create_user(workspace, 'admin', 'admin', True, ["*"], ["*"])

    print('New golem test directory created at {}'.format(workspace))
    print('Use credentials to access the GUI module:')
    print('user: admin')
    print('password: admin')


def create_user(workspace, username, password, is_admin, projects, reports):
    errors = []
    with open(os.path.join(workspace, 'users.json')) as users_file:
        try:
            user_data = json.load(users_file)
        except:
            user_data = []
    for user in user_data:
        if user['username'] == username:
            errors.append('username {} already exists'.format(username))
            break
    if not errors:
        new_user = {
            'id': str(uuid.uuid4())[:8],
            'username': username,
            'password': password,
            'is_admin': is_admin,
            'gui_projects': projects,
            'report_projects': reports
        }
        user_data.append(new_user)
        with open(os.path.join(workspace, 'users.json'), 'w') as users_file:
            json.dump(user_data, users_file, indent=4)

    return errors


def delete_element(workspace, project, element_type, dot_path):
    """Delete a test, page or suite given it's full path
    separated by dots.
    """
    if element_type == 'test':
        folder = 'tests'
    elif element_type == 'page':
        folder = 'pages'
    elif element_type == 'suite':
        folder = 'suites'
    else:
        raise Exception('Incorrect element type')

    errors = []
    path = os.path.join(workspace, 'projects', project, folder,
                        dot_path.replace('.', os.sep) + '.py')
    if not os.path.exists(path):
        errors.append('File {} does not exist'.format(dot_path))
    else:
        try:
            os.remove(path)
        except:
            errors.append('There was an error removing file {}'.format(dot_path))

    if element_type == 'test':
        # TODO deprecate data folder
        data_path = os.path.join(workspace, 'projects', project, 'data',
                                 dot_path.replace('.', os.sep) + '.csv')
        try:
            os.remove(data_path)
        except:
            pass
        data_path = os.path.join(workspace, 'projects', project, 'tests',
                                 dot_path.replace('.', os.sep) + '.csv')
        try:
            os.remove(data_path)
        except:
            pass

    return errors


def duplicate_element(workspace, project, element_type, original_file_dot_path,
                      new_file_dot_path):
    errors = []
    if element_type == 'test':
        folder = 'tests'
    elif element_type == 'page':
        folder = 'pages'
    elif element_type == 'suite':
        folder = 'suites'
    else:
        errors.append('Element type is incorrect')
    if not errors:
        if original_file_dot_path == new_file_dot_path:
            errors.append('New file cannot be the same as the original')
        for c in new_file_dot_path.replace('.', ''):
            if not c.isalnum() and c != '_':
                errors.append('Only letters, numbers and underscores are allowed')
                break

    if not errors:
        root_path = os.path.join(workspace, 'projects', project)
        original_file_rel_path = original_file_dot_path.replace('.', os.sep) + '.py'
        original_file_full_path = os.path.join(root_path, folder, original_file_rel_path)
        new_file_rel_path = new_file_dot_path.replace('.', os.sep) + '.py'
        new_file_full_path = os.path.join(root_path, folder, new_file_rel_path)
        if os.path.exists(new_file_full_path):
            errors.append('A file with that name already exists')

    if not errors:
        try:
            file_manager.create_directory(path=os.path.dirname(new_file_full_path), add_init=True)
            shutil.copyfile(original_file_full_path, new_file_full_path)
        except:
            errors.append('There was an error creating the new file')

    if not errors and element_type == 'test':
        # TODO deprecate data folder
        try:
            original_data_rel_path = original_file_dot_path.replace('.', os.sep) + '.csv'
            original_data_full_path = os.path.join(root_path, 'data', original_data_rel_path)
            new_data_rel_path = new_file_dot_path.replace('.', os.sep) + '.csv'
            new_data_full_path = os.path.join(root_path, 'data', new_data_rel_path)
            os.makedirs(os.path.dirname(new_data_full_path), exist_ok=True)
            shutil.copyfile(original_data_full_path, new_data_full_path)
        except:
            pass
        try:
            original_data_rel_path = original_file_dot_path.replace('.', os.sep) + '.csv'
            original_data_full_path = os.path.join(root_path, 'tests', original_data_rel_path)
            new_data_rel_path = new_file_dot_path.replace('.', os.sep) + '.csv'
            new_data_full_path = os.path.join(root_path, 'tests', new_data_rel_path)
            file_manager.create_directory(path=os.path.dirname(new_data_full_path), add_init=True)
            shutil.copyfile(original_data_full_path, new_data_full_path)
        except:
            pass

    return errors


def choose_browser_by_precedence(cli_browsers=None, suite_browsers=None,
                                 settings_default_browser=None):
    """ Defines which browser(s) to use by order of precedence
    The order is the following:
    1. browsers defined by CLI
    2. browsers defined inside a suite
    3. 'default_driver' setting
    4. chrome
    """
    if cli_browsers:
        browsers = cli_browsers
    elif suite_browsers:
        browsers = suite_browsers
    elif settings_default_browser:
        browsers = [settings_default_browser]
    else:
        browsers = ['chrome']  # default default
    return browsers


# TODO
def load_json_from_file(filepath, ignore_failure=False, default=None):
    json_data = default
    with open(filepath) as json_file:
        try:
            contents = json_file.read()
            if len(contents.strip()):
                json_data = json.loads(contents)
        except Exception as e:
            msg = 'There was an error parsing file {}'.format(filepath)
            print(msg)
            print(traceback.format_exc())
            if not ignore_failure:
                raise Exception(msg).with_traceback(e.__traceback__)
    return json_data


def import_module(path):
    """Import a Python module from a given path"""
    mod = None
    error = None
    module_dir, module_file = os.path.split(path)
    module_name, module_ext = os.path.splitext(module_file)
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        # Note: module_from_spec is new in python 3.5
        if hasattr(importlib.util, 'module_from_spec'):
            _mod = importlib.util.module_from_spec(spec)
        else:
            _mod = spec.loader.load_module()
        spec.loader.exec_module(_mod)
        mod = _mod
    except:
        error = traceback.format_exc(limit=0)
    return mod, error


def extract_version_from_webdriver_filename(filename):
    """Extract version from webdriver filename.
    
    Expects a file in the format: `filename_1.2` or `filename_1.2.exe`
    The extracted version must conform with pep-386
    If a valid version is not found it returns '0.0'
    """
    version = '0.0'
    if '_' in filename:
        components = filename.replace('.exe', '').split('_')
        if len(components) > 1:
            parsed_version = components[-1]
            try:
                StrictVersion(parsed_version)
                version = parsed_version
            except:
                pass
    return version


def match_latest_executable_path(glob_path):
    """Returns the absolute path to the webdriver executable
    with the highest version given a path with glob pattern.
    """
    found_files = []
    absolute_glob_path = os.path.abspath(glob_path)
    # Note: recursive=True arg is not supported
    # in Python 3.4, so '**' wildcard is not supported
    matched_files = glob.glob(absolute_glob_path)
    for matched_file in matched_files:
        found_files.append((matched_file, extract_version_from_webdriver_filename(matched_file)))
    if found_files:
        highest_version = sorted(found_files, key=lambda tup: StrictVersion(tup[1]), reverse=True)
        return highest_version[0][0]
    else:
        return None


def get_valid_filename(s):
    """Receives a string and returns a valid filename"""
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def prompt_yes_no(question, default=True):
    """Prompt the user through the console for yes or no"""
    while True:
        choice = input(question).lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        elif not choice:
            return default


class ImmutableKeysDict(dict):
    """A dictionary where keys cannot be added after instantiation"""

    def __setitem__(self, key, value):
        if key not in self:
            raise AttributeError("cannot add new keys to ImmutableKeysDict")
        dict.__setitem__(self, key, value)

