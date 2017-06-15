"""
A Python client for interacting with the Center for Responsive Politics' 
campaign finance data.

API docs: https://www.opensecrets.org/resources/create/api_doc.php
"""

import httplib2
import json
import os
import urllib, urllib2


class CRPError(Exception):
    """ Exception for general CRP Client errors. """
    def __init__(self, message, response=None, url=None):
        super(CRPError, self).__init__(message)
        self.message = message
        self.response = response
        self.url = url


class Client(object):

    BASE_URI = \
            'https://www.opensecrets.org/api/?method={method}&output=json&apikey={apikey}&{params}'

    def __init__(self, apikey=None, cache='.cache'):

        self.apikey = apikey
        self.http = httplib2.Http(cache)

    def fetch(self, method, **kwargs):
        """ Make the API request. """

        params = urllib.urlencode(kwargs)
        url = self.BASE_URI.format(method=method, apikey=self.apikey, params=params)
        headers = { 'User-Agent' : 'Mozilla/5.0' }

        resp, content = self.http.request(url, headers=headers)
        content = json.loads(content)

        if not resp.get('status') == '200':
            raise CRPError(method, resp, url)

        return content['response']


class CandidatesClient(Client):

    def get(self, id_code):
        """ 
            id_code may be either a candidate's specific CID, or a two letter 
            state code, or a 4 character district code.
        """
        return self.fetch('getLegislators', id=id_code)['legislator']

    def pfd(self, cid, year=None):
        kwargs = {'cid' : cid}

        if year:
            kwargs['year'] = year

        return self.fetch('memPFDprofile', **kwargs)['member_profile']

    def summary(self, cid, cycle=None):
        kwargs = {'cid' : cid}

        if cycle:
            kwargs['cycle'] = cycle

        return self.fetch('candSummary', **kwargs)['summary']['@attributes']

    def contrib(self, cid, cycle=None):
        kwargs = {'cid' : cid}

        if cycle:
            kwargs['cycle'] = cycle

        return self.fetch('candContrib', **kwargs)['contributors']['contributor']

    def industries(self, cid, cycle=None):
        kwargs = {'cid' : cid}

        if cycle:
            kwargs['cycle'] = cycle

        return self.fetch('candIndustry', **kwargs)['industries']['industry']

    def contrib_by_ind(self, cid, industry, cycle=None):
        kwargs = {'cid' : cid, 'ind' : industry}

        if cycle:
            kwargs['cycle'] = cycle

        return self.fetch('candIndByInd', **kwargs)['candIndus']['@attributes']

    def sector(self, cid, cycle=None):
        kwargs = {'cid' : cid}

        if cycle:
            kwargs['cycle'] = cycle

        return self.fetch('candSector', **kwargs)['sectors']['sector']


class CommitteesClient(Client):

    def cmte_by_ind(self, cmte, industry, congress=None):
        kwargs = {'cmte' : cmte, 'indus' : industry}

        if congress:
            kwargs['congno'] = congress

        return self.fetch('congCmteIndus', **kwargs)['committee']['@attributes']


class OrganizationsClient(Client):

    def get(self, org_name):
        return self.fetch('getOrgs', org=org_name)['organization']

    def summary(self, org_id):
        return self.fetch('orgSummary', id=org_id)['organization']['@attributes']


class CRP(Client):

    def __init__(self, apikey=None, cache='.cache'):

        if apikey is None:
            apikey = os.environ.get('OPENSECRETS_API_KEY')

        super(CRP, self).__init__(apikey, cache)
        self.candidates = CandidatesClient(self.apikey, cache)
        self.committees = CommitteesClient(self.apikey, cache)
        self.orgs = OrganizationsClient(self.apikey, cache)
