from typing import Union
from collections import namedtuple
from flask import render_template
from flask import current_app as app
from flask import request

from hubgrep.constants import SITE_TITLE, PARAM_OFFSET, PARAM_PER_PAGE
from hubgrep.lib.pagination import get_page_links
from hubgrep.lib.fetch_results import fetch_concurrently
from hubgrep.lib.filter_results import filter_results
from hubgrep.lib.get_hosting_service_interfaces import get_hosting_service_interfaces
from hubgrep.models import HostingService

from hubgrep.frontend_blueprint import frontend

checkbox = namedtuple("checkbox", "id label is_checked")
search_form = namedtuple("form", "search_phrase services allow_forks allow_archived")


def _get_search_form(search_phrase: Union[str, bool], allow_forks: bool, allow_archived: bool) -> search_form:
    service_checkboxes = []
    for service in HostingService.query.all():
        is_checked = search_phrase is False or request.args.get("s{}".format(service.id), False) == "on"
        service_checkboxes.append(checkbox(id="s{}".format(service.id), label="{} - {}".format(service.landingpage_url, service.type),
                                           is_checked=is_checked))  # TODO add label to service name instead of landingpage_url

    return search_form(search_phrase=search_phrase, services=service_checkboxes,
                       allow_forks=allow_forks, allow_archived=allow_archived)


@frontend.route("/")
def index():
    results_paginated = []
    results_offset = int(request.args.get(PARAM_OFFSET, 0))
    results_per_page = int(request.args.get(PARAM_PER_PAGE, app.config['PAGINATION_PER_PAGE_DEFAULT']))
    search_phrase = request.args.get("s", False)
    allow_forks = search_phrase is False or request.args.get("f", False) == "on"
    allow_archived = search_phrase is False or request.args.get("a", False) == "on"
    search_feedback = ""
    external_errors = []
    pagination_links = []
    if search_phrase is not False:
        terms = search_phrase.split()
        search_interfaces = get_hosting_service_interfaces(cache=app.config['ENABLE_CACHE'])
        results, external_errors = fetch_concurrently(terms, search_interfaces)
        results = filter_results(results, )
        results_paginated = results[results_offset:(results_offset + results_per_page)]
        pagination_links = get_page_links(request.full_path, results_offset, results_per_page, len(results))
        search_feedback = "page {} of {} total matching repositories.".format(
            results_offset // results_per_page + 1, len(results))

    return render_template("search/search.html",
                           title=SITE_TITLE,
                           search_results=results_paginated,
                           search_url=request.url,
                           search_phrase=search_phrase,
                           search_feedback=search_feedback,
                           form=_get_search_form(search_phrase, allow_forks, allow_archived),
                           pagination_links=pagination_links,  # [PageLink] namedtuples
                           external_errors=external_errors)  # TODO these errors should be formatted to text that is useful for a enduser
