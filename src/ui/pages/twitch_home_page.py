from typing import Any

import allure
from selenium.webdriver.support.wait import WebDriverWait

from ui.pages.base_page import BasePage


class TwitchHomePage(BasePage):

    def __init__(self, driver, wait: WebDriverWait, locators: Any):
        super().__init__(driver, wait)
        self.loc = locators

    @allure.step("Open searched element by index: {index}")
    def select_resources_by_index(self, index: int) -> "TwitchHomePage":
        self.click_by_index(self.loc.SEARCH_RESULTS, index)
        return self


class TwitchHomePageMobile(TwitchHomePage):
    @allure.step('Search text (mobile): "{text}"')
    def search_by_text(self, text: str) -> "TwitchHomePageMobile":
        self.click(self.loc.SEARCH_WINDOW)
        self.click(self.loc.SEARCH_INPUT)
        self.fill_text(self.loc.SEARCH_INPUT, text)
        return self


class TwitchHomePageDesktop(TwitchHomePage):
    @allure.step('Search text (desktop): "{text}"')
    def search_by_text(self, text: str) -> "TwitchHomePageDesktop":
        self.click(self.loc.SEARCH_INPUT)
        self.fill_text(self.loc.SEARCH_INPUT, text)
        return self
