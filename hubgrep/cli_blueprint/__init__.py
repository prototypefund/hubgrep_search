from flask import Blueprint

cli_bp = Blueprint("cli", __name__)

from hubgrep.cli_blueprint.version import version
from hubgrep.cli_blueprint.search import search
from hubgrep.cli_blueprint.read_hosters_json import add_hosters, list_hosters
from hubgrep.cli_blueprint.init import init
from hubgrep.cli_blueprint.add_hoster import add_hoster
from hubgrep.cli_blueprint.build_scss import build_scss
from hubgrep.cli_blueprint.copy_static import copy_static
