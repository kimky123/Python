import time

class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def fill_form_by_css(self, form_css, value):
        elem = self.driver.find(form_css)
        elem.send_keys(value)

    def fill_form_by_id(self, form_element_id, value):
        return self.fill_form_by_css('#%s' % form_element_id, value)

    def fill_form_by_xpath(self, form_xpath, value):
        elem = self.driver.find_element_by_xpath(form_xpath)
        elem.send_keys(value)

    def navigate(self):
        self.driver.get(self.url)

    def refresh(self):
        self.driver.refresh()

    def navBack(self):
        self.driver.back()

class Homepage(BasePage):
    url = 'http://www.moat.com'

    def setInput(self, form_xpath, value):
        self.fill_form_by_xpath(form_xpath, value)

    def submitSearch(self, form_xpath):
        elem = self.driver.find_element_by_xpath(form_xpath)
        elem.click()

    def getTryThese(self, form_xpath):
        elem = self.driver.find_elements_by_xpath(form_xpath)
        tryThese = []
        for link in elem:
            tryThese.append(link.text)
        return tryThese

    def getAdTime(self, recentAd, seenTime):
        ad = self.driver.find_element_by_xpath(recentAd)
        ad.click()
        timeText = self.driver.find_element_by_xpath(seenTime).text
        self.navBack()
        subStringBeg = "seen "
        subStringEnd = " ago"
        timeText = timeText[timeText.index(subStringBeg)+5:timeText.index(subStringEnd)]
        return timeText
            
    def getRecentAdsCount(self, ads):
        recentAds = self.driver.find_elements_by_xpath(ads)
        adCount = len(recentAds)
        return adCount

    def assertCompareAdTime(self, adTimeTexts):
        results = []
        for adText in adTimeTexts:
            lessThan30 = True
            if "hours" in adText:
                lessThan30 = False
            elif "minutes" in adText:
                adText = adText[:adText.index(" ")]
                adTime = int(adText)
                if(adTime < 30):
                    lessThan30 = True
                else:
                    lessThan30 = False
            results.append(lessThan30)
        return results  
        
class ResultsPage(BasePage):
    def adSummaryCount (self, locator):
        countStr = self.driver.find_element_by_xpath(locator).text
        countStr = countStr[:countStr.index(" ads")]
        countStr = countStr.replace(',', '')
        countInt = int(countStr)
        return countInt
    
    def getCountActual(self, dispCountLoc, showMoreLoc, adsLoc):
        dispCount = self.adSummaryCount(dispCountLoc)
        if(dispCount > 100):
            print "Total ad count is more than 100-- Navigating..."
            pageCount = int(dispCount/100)
            for i in range (0, pageCount):
                elem = self.driver.find_element_by_xpath(showMoreLoc)
                displayed = elem.is_displayed() 
                if displayed:
                    elem.click()
                    ##probably need to implement a better way to wait than this
                    time.sleep(1)
        else:
            print "Total ad count is less than or equal to 100!"
        ads = self.driver.find_elements_by_xpath(adsLoc)
        adCount = len(ads)
        return adCount
    
    def clickFirstAd (self, firstAdLoc):
        firstAd = self.driver.find_element_by_xpath(firstAdLoc)
        firstAd.click()

    def getFirstAdId (self, firstAdLoc):
        firstAd = self.driver.find_element_by_xpath(firstAdLoc)
        firstAdId = firstAd.get_attribute("creativeid")
        return firstAdId

    def clickShareThis(self, shareThisLoc, linkLoc):
        shareThis = self.driver.find_element_by_xpath(shareThisLoc)
        shareThis.click()
        linkElem = self.driver.find_element_by_xpath(linkLoc)
        linkAddress = linkElem.get_attribute("value")
        return linkAddress
        
        
