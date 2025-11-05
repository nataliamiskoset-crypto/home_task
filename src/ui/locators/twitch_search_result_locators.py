from selenium.webdriver.common.by import By


class TwitchSearchResultLocatorsDesktop:
    LIVE_CHANNEL_RESULTS: tuple[str, str] = (By.CSS_SELECTOR, '[data-a-target="search-result-live-channel"]')
    LIVE_CHANNEL_RESULTS_TITLE= (By.CSS_SELECTOR, '[data-test-selector="search-result-live-channel__name"]')


class TwitchSearchResultLocatorsMobile:
    LIVE_CHANNEL_RESULTS: tuple[str, str] = (By.CSS_SELECTOR, 'div[role="list"] button')
    SHOW_ALL_VIDEOS = (By.CSS_SELECTOR, 'a[class*="ScCoreLink"][href*="/search"]')
    LIVE_CHANNEL_RESULTS_TITLE: tuple[str, str] = (By.CSS_SELECTOR, 'h2[title]')


