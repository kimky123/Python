from selenium.webdriver.common.by import By

class MainPageLocators(object):
    searchField = '//div[@id="search-box"]//input'
    submitButton = '//div[@id="search-box"]/input[@id="search-btn"]'
    tryThese = '//div[@id="search-suggestions-box"]/a'
    recentAds = '//div[@id="search-sub"]//li[@class="featured-agencies"]//a'
    @classmethod
    def recentAd(self, nth):
        ad = '//div[@id="search-sub"]//li[@class="featured-agencies"][' + str(nth) + ']//a'
        return ad

class SearchResultsPageLocators(object):
    adTime = '//div[@id="fancybox-content"]//table[contains(@id, "popup-container-hilight")]//div[@title="Ad Found On"]'
    moreButton = '//div[@class="next-page-button"]//button[@class="btn"]'
    ads = '//div[@class="adcontainer"]//img'
    summary = '//p[@class="query-summary"]'
    firstAd = '//div[@class="column"][1]/div[@class="adcontainer"][1]//img'
    firstAdId = '//div[@class="column"][1]/div[@class="adcontainer"][1]/div'
    shareThis = '//table[contains(@id, "popup-container")]//a[text()="Share this ad"]'
    linkAddress = '//div[@title="Share"]/input[@class="share-this-ad"]'
