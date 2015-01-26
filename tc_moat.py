import unittest
from locators import *
from pageObjects import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestMoat(unittest.TestCase):

    def setUp(self):
        ##access the website
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.homepage = Homepage(self.driver)
        self.homepage.navigate()
        ##verify the website title
        self.assertIn('Moat Ad Search', self.driver.title)

    def test_try_these_is_random(self):
        print "Verify that the 'Try These' links are random and that they work."
        ##fetch the try these link values
        tryTheseBefore = self.homepage.getTryThese(MainPageLocators.tryThese)
        print "Try these brands before the refresh: "
        print tryTheseBefore
        ##refresh the page and then fetch the try these link values again
        self.homepage.refresh()
        tryTheseAfter= self.homepage.getTryThese(MainPageLocators.tryThese)
        print "Try these brands after the refresh: "
        print tryTheseAfter
        ##compare the try these link values before and after the refresh and verify them to be different
        self.assertNotEqual(tryTheseBefore, tryTheseAfter, "Testing to see the try these are random")

    def test_recently_seen_ads(self):
        print "Verify that the 'Recently Seen Ads' are no more than half an hour old."
        ##fetch the ad time texts of each recently seen ad
        adCount = self.homepage.getRecentAdsCount(MainPageLocators.recentAds)
        adTimeTexts = []
        for i in range(1,adCount):
            text = self.homepage.getAdTime(MainPageLocators.recentAd(i), SearchResultsPageLocators.adTime)
            adTimeTexts.append(text)
        print "These are the times of the recently seen ads: "
        print adTimeTexts
        
        ##check each ad time to see if it exceeds 30 minutes
        results = self.homepage.assertCompareAdTime(adTimeTexts)
        for compare in results:
            self.assertTrue(compare, "Testing to see if the recent ad times are less than 30 minutes")

    def test_verify_ad_count(self):
        print "Verify that the ad counts are correct, even when they are over 100."
        ##Search for Samsung
        enterSearch = self.homepage.setInput(MainPageLocators.searchField, 'Samsung')
        submitSearch = self.homepage.submitSearch(MainPageLocators.submitButton)

        ##Get the count from the summary text and compare against the # of actual ads shown
        resultsPage = ResultsPage(self.driver)
        adSummary = resultsPage.adSummaryCount(SearchResultsPageLocators.summary)
        print "Ads count displayed in the summary: "
        print adSummary
        actualAdCount = resultsPage.getCountActual(SearchResultsPageLocators.summary,SearchResultsPageLocators.moreButton, SearchResultsPageLocators.ads)
        print "Ads count actually fetched: "
        print actualAdCount
        self.assertEqual(adSummary, actualAdCount, "Get the count from the summary text and compare against the # of actual ads shown")

    def test_share_this_ad(self):
        print "Verify the 'Share this Ad' feature."
        ##Search for Samsung
        enterSearch = self.homepage.setInput(MainPageLocators.searchField, 'Samsung')
        submitSearch = self.homepage.submitSearch(MainPageLocators.submitButton)

        resultsPage = ResultsPage(self.driver)
        ##Click on the first ad on the results page
        resultsPage.clickFirstAd(SearchResultsPageLocators.firstAd)
        firstAdId = resultsPage.getFirstAdId(SearchResultsPageLocators.firstAdId)
        
        linkAddress = resultsPage.clickShareThis(SearchResultsPageLocators.shareThis, SearchResultsPageLocators.linkAddress)
        print "This is the link address from 'Share This': "
        print linkAddress
        expectedAddress = "http://www.moat.com/search/results?brand[0]=samsung&ad=" + firstAdId
        self.assertEqual(expectedAddress,linkAddress, "Compare that the share this address matches the expected link address")

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
