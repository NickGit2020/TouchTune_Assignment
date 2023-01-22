import requests
import unittest
import json
from types import SimpleNamespace

class DiscogsArtistsSearchTest(unittest.TestCase):

    def setUp(self):
        self.baseSearchUrl = "https://api.discogs.com/database/search?artist=nirvana"
        self.token = "&token=TKMsBKoGscUmIROCQIBDEuSvNjEKrHEwsixLVjHy"

    def test_itShouldSearchSuccessfullyWhenValidCredentialsAreUsed(self):
        resp = requests.get(self.baseSearchUrl +"&page=1&per_page=75" + self.token)
        assert resp.status_code == 200, "Authentication failed with valid token"

    def test_itShouldFailToSearchWhenInvalidCredentialsAreSupplied(self):
       resp = requests.get(self.baseSearchUrl +"&page=1&per_page=75" + "INVALID")
       assert resp.status_code == 401, "User has successfully searched an artist record with an invalid token supplied"
       assert resp.json()['message'] == "You must authenticate to access this resource.", 'The fail message is Invalid'

    def test_itShouldReturnDefaultPerPageCountWhenNoPaginationLimitsAreSupplied(self):
        resp = requests.get(self.baseSearchUrl + self.token)
        defaultCount = 50
        countedResults = len(resp.json()['results'])
        assert resp.json()['pagination']['per_page'] == defaultCount, 'Default response is not '+ str(defaultCount) + ' per page'
        assert countedResults == defaultCount, 'Counted Results:' + str(countedResults) + ' not equal to default count: ' + str(defaultCount)

    def test_itShouldReturnPaginationCountMatchingSearchQueries(self):
       perPageResult = 75
       resp = requests.get(self.baseSearchUrl + "&page=1&per_page=" + str(perPageResult) +self.token)
       countedResult = len(resp.json()['results']);
       assert resp.json()['pagination']['per_page'] == perPageResult, 'could not get the Expected records per page'
       assert countedResult == perPageResult, 'Counted Results: '+ str(countedResult)  + ' did not match the requested value: ' + str(perPageResult)

    def test_itShouldReturnMaximumPerPageCountWhenPaginationLimtIsLarge(self):
       resp = requests.get(self.baseSearchUrl+"&page=1&per_page=120"+self.token)
       maximumPerPageCount = 100;
       countedResult = len(resp.json()['results']);
       assert resp.json()['pagination']['per_page'] == maximumPerPageCount, 'Response did not match the Maximum Limt of ' + maximumPerPageCount
       assert countedResult == maximumPerPageCount, 'Counted: ' + str(countedResult) + ' records when maximum should be: ' + str(maximumPerPageCount);

if __name__ == '__main__':
    unittest.main()