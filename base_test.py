from abc import ABC
from pprint import pprint

from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.support.wait import WebDriverWait

from ui.pages.base_page import BasePage
from ui.pages.locators.twitch_home_locators import TwitchHomeLocatorsMobile, TwitchHomeLocatorsDesktop
from ui.pages.locators.twitch_live_chanel_locators import TwitchLiveChanelLocatorsDesktop, TwitchLiveChanelLocatorsMobile
from ui.pages.locators.twitch_search_result_locators import TwitchSearchResultLocatorsDesktop, \
    TwitchSearchResultLocatorsMobile
from ui.pages.twitch_home_page import TwitchHomePageDesktop, TwitchHomePageMobile
from ui.pages.twitch_live_chanel_page import TwitchLiveChanelPageMobile, TwitchLiveChanelPageDesktop
from ui.pages.twitch_search_resault_page import TwitchSearchResultPageMobile, TwitchSearchResultPageDesktop


class BaseTest(ABC):
    driver: Chrome | Firefox | Edge
    wait: WebDriverWait
    twitch_home_page: object
    twitch_search_result_page: object
    twitch_live_chanel_page: object

    def handle_cookies(self):
        if hasattr(self, "driver") and hasattr(self, "wait"):
            BasePage(self.driver, self.wait).accept_cookies_if_present()
        else:
            pprint("⚠️ No driver or wait available for cookie handling.")

    def init_pages(self):
        self.wait = getattr(self, "wait", WebDriverWait(self.driver, 10))
        if self.emulator:
            self.twitch_home_page = TwitchHomePageMobile(self.driver, self.wait, TwitchHomeLocatorsMobile)
            self.twitch_search_result_page = TwitchSearchResultPageMobile(self.driver, self.wait, TwitchSearchResultLocatorsMobile)
            self.twitch_live_chanel_page = TwitchLiveChanelPageMobile(self.driver, self.wait, TwitchLiveChanelLocatorsMobile)
        else:
            self.twitch_home_page = TwitchHomePageDesktop(self.driver, self.wait, TwitchHomeLocatorsDesktop)
            self.twitch_search_result_page = TwitchSearchResultPageDesktop(self.driver, self.wait, TwitchSearchResultLocatorsDesktop)
            self.twitch_live_chanel_page = TwitchLiveChanelPageDesktop(self.driver, self.wait, TwitchLiveChanelLocatorsDesktop)

    def setup_method(self, method):
        self.init_pages()
        self.handle_cookies()
