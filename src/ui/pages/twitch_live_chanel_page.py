from time import sleep

import allure
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from ui.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class TwitchLiveChanelPage(BasePage):

    def __init__(self, driver, wait: WebDriverWait, locators):
        super().__init__(driver, wait)
        self.loc = locators

    @allure.step("Check and close pop-up if present")
    def check_pop_up(self, timeout: int = 30) -> bool:
        try:
            popup = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.loc.POP_UP)
            )
            popup.click()
            print("✅ Closed interfering pop-up window.")
            return True
        except TimeoutException:
            print("ℹ️ No pop-up detected on live page.")
            return False
        except StaleElementReferenceException:
            print("⚠️ Pop-up disappeared before clicking.")
            return False

    @allure.step("Verify channel is live (checking video + chat)")
    def verify_channel_is_live(self, timeout: int = 30) -> bool:
        self.check_pop_up()
        WebDriverWait(self.driver, timeout).until(
            EC.all_of(
                EC.visibility_of_element_located(self.loc.LIVE_VIDEO),
                EC.visibility_of_element_located(self.loc.LIVE_CHAT)
            )
        )
        if self.driver.find_elements(*self.loc.LIVE_VIDEO):
                return True
        raise RuntimeError("❌ The channel appears to be offline — no 'Live' badge or chat.")

class TwitchLiveChanelPageMobile(TwitchLiveChanelPage):
    @allure.step("Get channel title (mobile)")
    def get_channel_title(self) -> str:
        return self.driver.title.replace("- Twitch", "").strip()

class TwitchLiveChanelPageDesktop(TwitchLiveChanelPage):
    @allure.step("Get channel title (desktop)")
    def get_channel_title(self) -> str:
        el = self.find_element(self.loc.LIVE_TITLE)
        title = el.text.strip().replace("- Twitch", "")
        return title
