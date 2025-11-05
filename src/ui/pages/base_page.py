import datetime
import os
import time
from pathlib import Path
from pprint import pprint
from typing import Tuple, List

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains, Chrome, Edge, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class BasePage:
    def __init__(self, driver: Chrome | Firefox | Edge, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def find_elements(self, locator: tuple[str, str], min_count: int = 1, timeout: int = 10) -> List[WebElement]:
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise ValueError(f"❌ Invalid locator format: expected tuple(By, selector), got {locator!r}")

        custom_wait = WebDriverWait(self.driver, timeout, poll_frequency=0.2)
        custom_wait.until(lambda d: len(d.find_elements(*locator)) >= min_count)
        elems = self.driver.find_elements(*locator)
        if not elems:
            raise TimeoutException(f"❌ No elements found for {locator} after {timeout}s")
        return elems

    def find_element(self, locator: tuple[str, str], timeout: int = 10, scroll: bool = True) -> WebElement:
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(
            EC.presence_of_element_located(locator)
        )
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(EC.visibility_of(element))
        WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(EC.element_to_be_clickable(element))
        return element

    def click(self, locator: tuple[str, str], timeout: int = 15, retries: int = 2) -> None:
        last_err = None
        for attempt in range(retries + 1):
            try:
                el = self.find_element(locator, timeout=timeout)
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                try:
                    el.click()
                    return
                except (ElementClickInterceptedException, ElementNotInteractableException):
                    try:
                        self.driver.execute_script("arguments[0].click();", el)
                        return
                    except Exception as js_err:
                        last_err = js_err
                try:
                    ActionChains(self.driver).move_to_element(el).pause(0.05).click().perform()
                    return
                except Exception as action_err:
                    last_err = action_err
            except (StaleElementReferenceException, TimeoutException) as e:
                last_err = e

        raise RuntimeError(f"❌ Failed to click {locator} after {retries + 1} attempts: {last_err}")

    def fill_text(self, locator: tuple[str, str], txt: str) -> None:
        el: WebElement = self.find_element(locator, timeout=10)
        el.clear()
        el.send_keys(txt)

    def click_by_index(self, locator: tuple[str, str], index: int, timeout: int = 20):
        custom_wait = WebDriverWait(self.driver, timeout)
        elements = custom_wait.until(EC.presence_of_all_elements_located(locator))

        end_time = time.time() + timeout
        while len(elements) <= index and time.time() < end_time:
            time.sleep(0.5)
            elements = self.driver.find_elements(*locator)

        if index - 1 >= len(elements):
            raise IndexError(f"Index {index} out of range (found {len(elements)} elements)")

        element = elements[index - 1]
        self.wait.until(EC.element_to_be_clickable(element))
        ActionChains(self.driver).move_to_element(element).click().perform()

    def accept_cookies_if_present(self) -> None:
        cookie_locators = [
            (By.CSS_SELECTOR, 'button[data-a-target="consent-banner-accept"]'),
            (By.XPATH, "//button[contains(., 'Akceptuj') or contains(., 'Accept')]"),
            (By.CSS_SELECTOR, "button[aria-label*='Accept']"),
        ]
        for locator in cookie_locators:
            try:
                button = self.wait.until(EC.element_to_be_clickable(locator))
                button.click()
                pprint("🍪 Accepted cookies banner.")
                return True
            except TimeoutException:
                continue
        pprint("🍪 No cookie banner found.")
        return None

    def take_screenshot(self, folder_path: str = "screenshots", name_prefix: str = "screenshot") -> str:
        project_root = Path(__file__).resolve().parents[2]
        screenshot_dir = project_root / folder_path
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        file_path = screenshot_dir / f"{name_prefix}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        self.driver.save_screenshot(str(file_path))
        print(f"✅ Screenshot saved to: {file_path.resolve()}")
        return str(file_path.resolve())