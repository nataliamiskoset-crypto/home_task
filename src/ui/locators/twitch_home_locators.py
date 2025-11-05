from selenium.webdriver.common.by import By


class TwitchHomeLocatorsDesktop:
    SEARCH_INPUT: tuple[str, str] = (By.CSS_SELECTOR, 'input[aria-label="Pole wyszukiwania"]')
    SEARCH_RESULTS: tuple[str, str] = (By.CSS_SELECTOR, 'div[id^="search-result-row__"]')


class TwitchHomeLocatorsMobile:
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-a-target="tw-input"]')
    SEARCH_WINDOW = (By.CSS_SELECTOR, 'a[href="/directory"]')
    SEARCH_RESULTS = (By.CSS_SELECTOR, "ul > li")
