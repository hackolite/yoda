# This source file is part of Yoda.
#
# Yoda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yoda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yoda. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

from .config import Config
from .output import Output
from .repository import Repository, RepositoryError, \
    RepositoryPathInvalid, RepositoryAdapterNotFound
from .workspace import Workspace
from .subcommands import Subcommand, Subcommands


def find_path(name, config, wsonly=False):
    """ Find path for given workspace and|or repository """
    workspace = Workspace(config)
    config = config.get()["workspaces"]

    path_list = {}

    if name.find('/') != -1:
        wsonly = False
        ws, repo = name.split('/')
        if (workspace.exists(ws)):
            if (repo in config[ws]["repositories"]):
                path_name = "%s/%s" % (ws, repo)
                path_list[path_name] = config[ws]["repositories"][repo]

    for ws_name, ws in sorted(config.items()):
        if (name == ws_name):
            if wsonly is True:
                return {ws_name: ws["path"]}
            repositories = sorted(config[ws_name]["repositories"].items())
            for name, path in repositories:
                path_list["%s/%s" % (ws_name, name)] = path
            break

        for repo_name, repo_path in sorted(ws["repositories"].items()):
            if (repo_name == name):
                path_list["%s/%s" % (ws_name, repo_name)] = repo_path

    return path_list
