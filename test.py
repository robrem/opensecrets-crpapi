import httplib2
import json
import os
import urllib, urllib2
import unittest

from wr_crpapi import CRP

API_KEY = os.environ['OPENSECRETS_API_KEY']


class APITest(unittest.TestCase):

    def setUp(self):
        self.crp = CRP(API_KEY)
        self.http = httplib2.Http()

    def check_response(self, result, url, parse=''):
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        response = self.http.request(url, headers=headers)[1]
        response = json.loads(response)

        if callable(parse):
            response = parse(response)

        self.assertEqual(result, response)


class CandidatesTest(APITest):

    def test_get(self):
        pelosi = self.crp.candidates.get('N00007360')
        url = \
            'https://www.opensecrets.org/api/?method=getLegislators&output=json&id=N00007360&apikey={0}' \
            .format(API_KEY)

        self.check_response(pelosi, url, lambda r: r['response']['legislator'])

    def test_pfd(self):
        pfd = self.crp.candidates.pfd('N00007360')
        url = \
            'https://www.opensecrets.org/api/?method=memPFDprofile&output=json&cid=N00007360&apikey={0}' \
            .format(API_KEY)

        self.check_response(pfd, url, lambda r: r['response']['member_profile'])

    def test_summary(self):
        summ = self.crp.candidates.summary('N00007360', '2014')
        url = \
            'https://www.opensecrets.org/api/?method=candSummary&output=json&cid=N00007360&cycle=2014&apikey={0}' \
            .format(API_KEY)

        self.check_response(summ, url, lambda r: r['response']['summary']['@attributes'])

    def test_contrib(self):
        contrib = self.crp.candidates.contrib('N00007360', '2014')
        url = \
            'https://www.opensecrets.org/api/?method=candContrib&output=json&cid=N00007360&cycle=2014&apikey={0}' \
            .format(API_KEY)

        self.check_response(contrib, url, lambda r: r['response']['contributors']['contributor'])

    def test_industries(self):
        ind = self.crp.candidates.industries('N00007360', '2014')
        url = \
            'https://www.opensecrets.org/api/?method=candIndustry&output=json&cid=N00007360&cycle=2014&apikey={0}' \
            .format(API_KEY)

        self.check_response(ind, url, lambda r: r['response']['industries']['industry'])

    def test_contrib_by_ind(self):
        ind = self.crp.candidates.contrib_by_ind('N00007360', 'F10', '2014')
        url = \
            'https://www.opensecrets.org/api/?method=candIndByInd&output=json&cid=N00007360&cycle=2014&ind=F10&apikey={0}' \
            .format(API_KEY)

        self.check_response(ind, url, lambda r: r['response']['candIndus']['@attributes'])

    def test_sector(self):
        sector = self.crp.candidates.sector('N00007360', '2014')
        url = \
            'https://www.opensecrets.org/api/?method=candSector&output=json&cid=N00007360&cycle=2014&apikey={0}' \
            .format(API_KEY)

        self.check_response(sector, url, lambda r: r['response']['sectors']['sector'])


class CommitteesTest(APITest):

    def test_cmte_by_ind(self):
        cmte = self.crp.committees.cmte_by_ind('HARM', 'F10', '113')
        url = \
            'https://www.opensecrets.org/api/?method=congCmteIndus&output=json&cmte=HARM&indus=F10&congno=113&apikey={0}' \
            .format(API_KEY)

        self.check_response(cmte, url, lambda r: r['response']['committee']['@attributes'])


class OrganizationsTest(APITest):

    def test_get(self):
        org = self.crp.orgs.get('Goldman')
        url = \
            'https://www.opensecrets.org/api/?method=getOrgs&output=json&org=Goldman&apikey={0}' \
            .format(API_KEY)

        self.check_response(org, url, lambda r: r['response']['organization'])

    def test_summary(self):
        summ = self.crp.orgs.summary('D000000085')
        url = \
            'https://www.opensecrets.org/api/?method=orgSummary&output=json&id=D000000085&apikey={0}' \
            .format(API_KEY)

        self.check_response(summ, url, lambda r: r['response']['organization']['@attributes'])


if __name__ == '__main__':
    unittest.main()