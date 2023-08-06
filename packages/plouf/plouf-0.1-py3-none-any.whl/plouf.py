import click
import json
import os
import urllib.request
import importlib

import utils
import templates

# define plouffile name -- constant
plouf_files = {
    "config": ".plouffile",
    "templates": ".plouftemplates"
}

tests_frameworks = {
    'doctest': 'https://raw.githubusercontent.com/onqtam/doctest/master/doctest/doctest.h'
}

# Helper functions
def get_pf_path():
    """
    Returns plouffile full path
    """
    return utils.get_file_path(plouf_files["config"])

def get_project_types():
    """
    Returns array of possible projects (ones defines by implementation but also loaded from possible user templates)
    """
    types = [ "exec", "library" ]
    
    # trying to import custom ones
    user_tplt_path = utils.get_file_path(plouf_files["templates"])
    if os.path.exists(user_tplt_path):
        templates_module = importlib.import_module(user_tplt_path)
        # TODO: read custom templates from this file

    return types

def valid_repo():
    """
    Returns boolean if current repository has already been initialized.
    """
    return os.path.exists(get_pf_path())

def make_templates(files, target_name, override_flag):
    s = ""
    name = target_name
    for f in files:
        if f["type"] == "cmake_base":
            s = templates.cmake_base
        elif f["type"] == "header_base":
            s = templates.header_base
            name = target_name.upper()
        elif f["type"] == "main_tests":
            s = templates.main_tests
        elif f["type"] == "main_sample":
            s = templates.main_sample

        if s:
            if not os.path.exists(f["path"]) or override_flag:
                with open(f["path"], 'w') as fp:
                    fp.write(s.format_map(utils.Default(project_name=name)))
        
    

def make_structure(target_name, what, add_tests, override_flag):
    """
    Depending on the target type what, creates the folder structure.
    """
    rel_paths = [ target_name ]
    files = [
        { "type": "cmake_base", "path": os.path.join(target_name, "CMakeLists.txt") }
    ]
    
    if what == "exec":
        sample_path = os.path.join(target_name, "sample")
        rel_paths += [
            sample_path,
            os.path.join(target_name, "src")
            ]
        files.append({ "type": "main_sample", "path": os.path.join(sample_path, "main.cpp") })
    elif what == "library":
        include_path = os.path.join(target_name, "include", target_name)
        rel_paths += [
            include_path,
            os.path.join(target_name, "src")
        ]
        files.append({ "type": "header_base", "path": os.path.join(include_path, target_name + ".hpp") })
    
    if add_tests:
        tests_path = os.path.join(target_name, "tests")
        rel_paths.append(tests_path)
        files.append({ "type": "main_tests", "path": os.path.join(tests_path, "main_tests.cpp") })
    
    paths = [ utils.get_file_path(k) for k in rel_paths ]

    # creating folders
    utils.mkdirp(paths)

    # creating templates
    make_templates(files, target_name, override_flag)

# autocompletes

def autocomplete_project_types(ctx, args, incomplete):
    return [ k for k in get_project_types() if k.startswith(incomplete) ]

# Actual CLI
@click.group()
def main():
    """
    CLI tools for project creation.
    """
    pass

@main.command()
def init():
    """
    Initialize plouf project for this repository, creating plouffile.
    """

    if not valid_repo():
        click.confirm('A \"%s\" has been found in this repository, override it?' % plouf_files["config"], abort=True, prompt_suffix='')

    data = {
        'name': click.prompt('project name', default=utils.get_dirname()),
        'description': click.prompt('description', default=''),
        'author': click.prompt('author', default=''),
        'version': click.prompt('version', default='0.1.0')
    }

    click.echo(json.dumps(data, indent=2))
    click.confirm('Is this ok?', default=True, abort=True)
    
    try:
        with open(get_pf_path(), 'w') as pf:
            json.dump(data, pf, indent=4)
        
        utils.success('Initialized empty plouf repository.')

    except Exception as e:
        click.echo(
            click.style(e, fg="red"),
            err=True
        )

    pass


@main.command()
@click.option('--override', '-o', is_flag=True, default=False, help='Rewrite existing files if any with base templates.')
def setup(override):
    """
    Setup repository according to the plouffile.
    """
    if not valid_repo():
        utils.error('Not a plouf repository. (No \'.plouffile\' file found.)')
        return
    
    try:
        data = {}
        with open(get_pf_path(), 'r') as pf:
            data = json.load(pf)
        
        for name, proj in data.setdefault("projects", {}).items():
            make_structure(name, proj.setdefault("type", "exec"), proj.setdefault("tests", False), override)
            utils.info('Creating structure for %s...' % name)
            utils.list_files(utils.get_file_path(name))
        
        extern_path = utils.get_file_path("extern")
        if "tests" in data:
            utils.mkdirp([extern_path])

            for _, framework_url in data["tests"].items():
                file_path = os.path.join(extern_path, os.path.basename(framework_url))

                if os.path.exists(file_path):
                    utils.warning('%s file already exists.' % file_path)
                    if not click.confirm('Do you want to override it', prompt_suffix='?'):
                        continue
                utils.info('Fetching %s...' % framework_url, nl=False)
                urllib.request.urlretrieve(framework_url, file_path)
                click.echo('[OK]')
        
        utils.success('Setup complete.')
        
    except Exception as e:
        click.echo(
            click.style(e, fg="red"),
            err=True
        )
    

@main.command()
@click.argument('what', type=click.Choice(get_project_types()), autocompletion=autocomplete_project_types)
def add(what):
    """
    Adding an executable, library or test project.
    """
    if not valid_repo():
        utils.error('Not a plouf repository. (No \'%s\' file found.)' % plouf_files["config"])
        return

    try:
        data = {}
        name = click.prompt('%s name' % what, type=click.STRING)

        with open(get_pf_path(), 'r') as pf:
            data = json.load(pf)

        if not "projects" in data:
            data["projects"] = {}
        
        if name in data["projects"]:
            utils.warning('A project with this name already exists.')
            click.confirm('Do you want to override it', prompt_suffix='?', abort=True)

        data["projects"][name] = { "type": what }
        
        add_tests = click.confirm('create tests', prompt_suffix='?', default=True)
        if add_tests:
            f_name = click.prompt('test framework', type=click.STRING, default='doctest')
            f_url = click.prompt('header url', type=click.STRING, default=tests_frameworks[f_name])

            data.setdefault("tests", {})[f_name] = f_url
            data["projects"][name]["tests"] = True


        with open(get_pf_path(), 'w') as pf:
            json.dump(data, pf, indent=4)
        
        utils.success('Project added successfully.')

    except Exception as e:
        click.echo(
            click.style(e, fg="red"),
            err=True
        )

    pass

