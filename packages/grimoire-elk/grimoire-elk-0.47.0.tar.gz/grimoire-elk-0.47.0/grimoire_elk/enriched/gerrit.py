# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2019 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#   Alvaro del Castillo San Felix <acs@bitergia.com>
#

from datetime import datetime
from dateutil import parser
import logging
import time

from .enrich import Enrich, metadata
from ..elastic_mapping import Mapping as BaseMapping


logger = logging.getLogger(__name__)


class Mapping(BaseMapping):

    @staticmethod
    def get_elastic_mappings(es_major):
        """Get Elasticsearch mapping.

        :param es_major: major version of Elasticsearch, as string
        :returns:        dictionary with a key, 'items', with the mapping
        """

        mapping = """
        {
            "properties": {
               "status": {
                  "type": "keyword"
               },
               "summary_analyzed": {
                  "type": "text"
               },
               "timeopen": {
                  "type": "double"
               }
            }
        }
        """

        return {"items": mapping}


class GerritEnrich(Enrich):

    mapping = Mapping

    def __init__(self, db_sortinghat=None, db_projects_map=None, json_projects_map=None,
                 db_user='', db_password='', db_host=''):
        super().__init__(db_sortinghat, db_projects_map, json_projects_map,
                         db_user, db_password, db_host)

        self.studies = []
        self.studies.append(self.enrich_demography)
        self.studies.append(self.enrich_onion)

    def get_field_author(self):
        return "owner"

    def get_fields_uuid(self):
        return ["review_uuid", "patchSet_uuid", "approval_uuid"]

    def get_sh_identity(self, item, identity_field=None):
        identity = {}
        for field in ['name', 'email', 'username']:
            identity[field] = None

        user = item  # by default a specific user dict is expected
        if 'data' in item and type(item) == dict:
            user = item['data'][identity_field]

        if 'name' in user:
            identity['name'] = user['name']
        if 'email' in user:
            identity['email'] = user['email']
        if 'username' in user:
            identity['username'] = user['username']
        return identity

    def get_project_repository(self, eitem):
        repo = eitem['origin']
        repo += "_" + eitem['repository']
        return repo

    def get_identities(self, item):
        """Return the identities from an item"""

        item = item['data']

        # Changeset owner
        user = item['owner']
        identity = self.get_sh_identity(user)
        yield identity

        # Patchset uploader and author
        if 'patchSets' in item:
            for patchset in item['patchSets']:
                user = patchset['uploader']
                identity = self.get_sh_identity(user)
                yield identity
                if 'author' in patchset:
                    user = patchset['author']
                    identity = self.get_sh_identity(user)
                    yield identity
                if 'approvals' in patchset:
                    # Approvals by
                    for approval in patchset['approvals']:
                        user = approval['by']
                        identity = self.get_sh_identity(user)
                        yield identity

        # Comments reviewers
        if 'comments' in item:
            for comment in item['comments']:
                user = comment['reviewer']
                identity = self.get_sh_identity(user)
                yield identity

    def get_item_id(self, eitem):
        """ Return the item_id linked to this enriched eitem """

        # The eitem _id includes also the patch.
        return eitem["_source"]["review_id"]

    def _fix_review_dates(self, item):
        ''' Convert dates so ES detect them '''

        for date_field in ['timestamp', 'createdOn', 'lastUpdated']:
            if date_field in item.keys():
                date_ts = item[date_field]
                item[date_field] = time.strftime('%Y-%m-%dT%H:%M:%S',
                                                 time.localtime(date_ts))
        if 'patchSets' in item.keys():
            for patch in item['patchSets']:
                pdate_ts = patch['createdOn']
                patch['createdOn'] = time.strftime('%Y-%m-%dT%H:%M:%S',
                                                   time.localtime(pdate_ts))
                if 'approvals' in patch:
                    for approval in patch['approvals']:
                        adate_ts = approval['grantedOn']
                        approval['grantedOn'] = \
                            time.strftime('%Y-%m-%dT%H:%M:%S',
                                          time.localtime(adate_ts))
        if 'comments' in item.keys():
            for comment in item['comments']:
                cdate_ts = comment['timestamp']
                comment['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S',
                                                     time.localtime(cdate_ts))

    @metadata
    def get_rich_item(self, item):
        eitem = {}  # Item enriched

        for f in self.RAW_FIELDS_COPY:
            if f in item:
                eitem[f] = item[f]
            else:
                eitem[f] = None
        eitem['closed'] = item['metadata__updated_on']
        # The real data
        review = item['data']
        self._fix_review_dates(review)

        # data fields to copy
        copy_fields = ["status", "branch", "url"]
        for f in copy_fields:
            eitem[f] = review[f]
        # Fields which names are translated
        map_fields = {"subject": "summary",
                      "id": "githash",
                      "createdOn": "opened",
                      "project": "repository",
                      "number": "number"
                      }
        for fn in map_fields:
            eitem[map_fields[fn]] = review[fn]
        eitem["summary_analyzed"] = eitem["summary"]
        eitem["summary"] = eitem["summary"][:self.KEYWORD_MAX_SIZE]
        eitem["name"] = None
        eitem["domain"] = None
        if 'name' in review['owner']:
            eitem["name"] = review['owner']['name']
            if 'email' in review['owner']:
                if '@' in review['owner']['email']:
                    eitem["domain"] = review['owner']['email'].split("@")[1]
        # New fields generated for enrichment
        eitem["patchsets"] = len(review["patchSets"])

        # Limit the size of comment messages
        if 'comments' in review:
            for comment in review['comments']:
                comment['message'] = comment['message'][:self.KEYWORD_MAX_SIZE]

        # Time to add the time diffs
        created_on = review['createdOn']
        if len(review["patchSets"]) > 0:
            created_on = review["patchSets"][0]['createdOn']

        created_on_date = parser.parse(created_on)
        eitem["created_on"] = created_on

        eitem["last_updated"] = review['lastUpdated']
        last_updated_date = parser.parse(review['lastUpdated'])

        seconds_day = float(60 * 60 * 24)
        if eitem['status'] in ['MERGED', 'ABANDONED']:
            timeopen = \
                (last_updated_date - created_on_date).total_seconds() / seconds_day
        else:
            timeopen = \
                (datetime.utcnow() - created_on_date).total_seconds() / seconds_day
        eitem["timeopen"] = '%.2f' % timeopen

        if self.sortinghat:
            eitem.update(self.get_item_sh(item))

        if self.prjs_map:
            eitem.update(self.get_item_project(eitem))

        eitem.update(self.get_grimoire_fields(review['createdOn'], "review"))

        return eitem

    def enrich_demography(self, ocean_backend, enrich_backend, date_field="grimoire_creation_date",
                          author_field="author_uuid"):

        super().enrich_demography(ocean_backend, enrich_backend, date_field, author_field=author_field)

    def enrich_onion(self, ocean_backend, enrich_backend,
                     no_incremental=False,
                     in_index='gerrit_onion-src',
                     out_index='gerrit_onion-enriched',
                     data_source='gerrit',
                     contribs_field='uuid',
                     timeframe_field='grimoire_creation_date',
                     sort_on_field='metadata__timestamp',
                     seconds=Enrich.ONION_INTERVAL):

        super().enrich_onion(enrich_backend=enrich_backend,
                             in_index=in_index,
                             out_index=out_index,
                             data_source=data_source,
                             contribs_field=contribs_field,
                             timeframe_field=timeframe_field,
                             sort_on_field=sort_on_field,
                             no_incremental=no_incremental,
                             seconds=seconds)
