#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gitlab import Gitlab
from re import sub, search, escape, findall
from argparse import ArgumentParser, RawTextHelpFormatter

GITLAB_URL = 'http://ipt-gitlab.ies.inventec:8081'
GITLAB_API_TOKEN = 'LuhHqKxMY7b4nESGRkmv'
GITLAB_API_HEADER = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}

def getProjects():
    lab = Gitlab(GITLAB_URL, GITLAB_API_HEADER["PRIVATE-TOKEN"])
    projects = lab.projects.list(all=True)
    return projects

def getProject(id=0, name=''):
    lab = Gitlab(GITLAB_URL, GITLAB_API_HEADER["PRIVATE-TOKEN"])
    try:
        if name and not id:
            project = [
                e for e in lab.projects.list(search=name) if e.name == name
            ][0]
        else:
            project = lab.projects.get(id)
        return project
    except:
        return None

def getReadme(project, ref='master'):
    b = project.files.blame(file_path='README.md', ref=ref)
    info = '\n'.join(['\n'.join(e["lines"]) for e in b if e["lines"]])
    return info

def searchReadme(content='', filter='', idx=1):
    content = [l for l in content.splitlines() if l.strip()]
    filters = [
        content[i+idx] for i, e in enumerate(content) if search(filter, e)
    ]
    if not filters:
        return ''
    if len(filters) > 1:
        return str(filters)
    return filters[0]

def getVerByReadme(name):
    try:
        return sub(
            r'[^(\d+\.){2}\d+]', '',
            searchReadme(getReadme(getProject(name=name)), '## Version')
        )
    except AttributeError:
        return ''

def getReadmeContent(readme, filter):
    content = [e for e in readme.split('\n---\n') if filter in e]
    if not content:
        return {}
    return sub(r'\n{0}\n\n|\n$'.format(escape(filter)), '', content[0])

def getReadmeCoverage(readme):
    content  = [e for e in readme.split('\n---\n') if '## Coverage' in e]
    if not content:
        return {}
    content  = sub(r'\n+', '\n', content[0])
    contents = content.splitlines()
    return {
        b[0]: {
            "platform": b[2],
            "project" : b[1]
        }
        for b in [
            [l.strip() for l in a.split('|')][1:]
            for a in [e for e in contents if search(r'^\| .*', e)][1:]
        ]
    }

def getReadmeAssociates(readme):
    content  = [e for e in readme.split('\n---\n') if '## Associates' in e]
    if not content:
        return {}
    content  = sub(r'\n+', '\n', content[0])
    contents = content.splitlines()
    return {
        "owner": [
            contents[i+1]
            for i, e in enumerate(contents)
            if 'PIC' in e
        ][0].split(' - ')[-1].strip(),
        "lte_name": [
            contents[i+1]
            for i, e in enumerate(contents)
            if 'Test Leader' in e
        ][0].split(' - ')[-1].strip(),
        "developer": [
            contents[i+1]
            for i, e in enumerate(contents)
            if 'Developer' in e
        ][0].split(' - ')[-1].strip(),
        "te_name": ';'.join([
            l.strip()
            for l in sub(
                r'\*\*Developer.*',
                '',
                ''.join([
                    content.splitlines()[i+1:]
                    for i, e in enumerate(content.splitlines())
                    if 'Tester' in e
                ][0])).split(' - ')
            if l.strip()
        ])
    }

def getReadmeValidation(readme):
    content  = [e for e in readme.split('\n---\n') if '## Validation' in e]
    if not content:
        return {}
    content  = sub(r'\n+', '\n', content[0])
    contents = content.splitlines()
    return {
        b[0]: {
            "name": b[0],
            "customer": "",
            "project": b[1],
            "platform": "",
            "reports": (
                findall(
                    r'\(.*.\)', b[4]
                )[0].replace('(', '').replace(')', '')
                if b[4] and b[4] != 'None'
                else ""
            ),
            "validation": "False",
            "result": b[3].replace('{+', ''). \
                           replace('+}', ''). \
                           replace('{-', ''). \
                           replace('-}', '').strip().lower(),
            "datetime": b[2]
        }
        for b in [
            [l.strip() for l in a.split('|')][1:]
            for a in [e for e in contents if search(r'^\| .*', e)][1:]
        ]
    }

def getReadmeTestingMethodology(readme):
    content = [
        e for e in readme.split('\n---\n') if '## Testing Methodology' in e
    ]
    if not content:
        return {}
    content = sub(r'\n+', '\n', content[0])
    contents = content.splitlines()
    return {
        findall(
            r'\[.*.\]', b[1]
        )[0].replace('[', '').replace(']', ''): {
            "bkm_name": b[0],
            "bkm_id": findall(
                r'\[.*.\]', b[1]
             )[0].replace('[', '').replace(']', ''),
            "bkm_link": findall(
                r'\(.*.\)', b[1]
            )[0].replace('(', '').replace(')', ''),
            "bkm_objective": b[2],
            "bkm_version": b[3]
        }
        for b in [
            [l.strip() for l in a.split('|') if l.strip()]
            for a in [e for e in contents if search(r'^\| .*', e)][1:]
        ]
    }

def getReadmeEstimate(readme):
    estimate = '0'
    estregex = r'\d+(\.\d+){0,}'
    try:
        estimate = search(estregex,
                          searchReadme(readme, '## Estimate')).group()
        return estimate
    except:
        return estimate

if __name__ == '__main__':

    # parser arguments
    parser = ArgumentParser(description='Get GitLab project instance.',
                               formatter_class=RawTextHelpFormatter)
    parser.add_argument('-p', '--project',
                        action='store', type=str,
                        default='SIT-Flask-API',
                        help='set project name' + 
                             '\n(default: "%(default)s")')
    parser.add_argument('-r', '--readme',
                        action='store_true',
                        help='get README content by specified project name')
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='get all project')
    parser.add_argument('-u', '--url',
                        action='store', type=str,
                        default=GITLAB_URL,
                        help='set GitLab url' + 
                             '\n(default: "%(default)s")')
    parser.add_argument('--private-token',
                        action='store', type=str,
                        default=GITLAB_API_TOKEN,
                        help="set API user's private token" + 
                             '\n(default: "%(default)s")')
    group1 = parser.add_argument_group('Single',
                                       'python3 %(prog)s -p "SIT-Flask-API"')
    group1 = parser.add_argument_group('README',
                                       'python3 %(prog)s -p "SIT-Flask-API" -r')
    group2 = parser.add_argument_group('All', 'python3 %(prog)s -a')
    args   = parser.parse_args()
    project = args.project
    get_readme = args.readme
    all = args.all
    GITLAB_URL = args.url
    GITLAB_API_TOKEN = args.private_token
    GITLAB_API_HEADER.update({"PRIVATE-TOKEN": GITLAB_API_TOKEN})

    if all:
        tmp = [print(p) for p in getProjects()]
    elif get_readme:
        print(getReadme(getProject(name=project)))
    else:
        print(getProject(name=project))

