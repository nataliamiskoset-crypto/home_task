from typing import Any

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage


class TwitchSearchResultPage(BasePage):

    def __init__(self, driver, wait: WebDriverWait, locators: Any):
        super().__init__(driver, wait)
        self.loc = locators

class TwitchSearchResultPageMobile(TwitchSearchResultPage):
    @allure.step("Select live channel by index (mobile): {index}")
    def select_live_channel_by_index(self, index: int, timeout: int = 30) -> str:
        self.click(self.loc.SHOW_ALL_VIDEOS)
        channels = self.find_elements(self.loc.LIVE_CHANNEL_RESULTS)
        if index >= len(channels):
            raise IndexError(f"There is no element at index {index}. Found only {len(channels)} elements.")

        title = channels[index].find_element(By.CSS_SELECTOR, "h2[title]").get_attribute("title")
        element = channels[index]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(element))
        ActionChains(self.driver).move_to_element(element).click().perform()
        return title

    pass

class TwitchSearchResultPageDesktop(TwitchSearchResultPage):
    @allure.step("Select live channel by index (desktop): {index}")
    def select_live_channel_by_index(self, index: int, timeout: int = 30) -> str:
        custom_wait = WebDriverWait(self.driver, timeout)
        custom_wait.until(lambda d: len(d.find_elements(*self.loc.LIVE_CHANNEL_RESULTS)) > index)
        elements = self.find_elements(self.loc.LIVE_CHANNEL_RESULTS)
        if index >= len(elements):
            raise IndexError(f"There is no element at index {index}. Found only {len(elements)} elements.")
        title = elements[index].find_element(*self.loc.LIVE_CHANNEL_RESULTS_TITLE).text
        element = elements[index]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(element))
        ActionChains(self.driver).move_to_element(element).click().perform()
        return title
