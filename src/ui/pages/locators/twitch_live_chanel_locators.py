from selenium.webdriver.common.by import By


class TwitchLiveChanelLocatorsDesktop:
    LIVE_VIDEO = (By.CSS_SELECTOR, '[data-a-target="player-overlay-click-handler"]')
    LIVE_VIDEO_ERROR = (By.CSS_SELECTOR, '[data-a-target="player-overlay-content-gate"]')
    LIVE_CHAT = (By.CSS_SELECTOR, '[data-test-selector="chat-room-component-layout"]')
    LIVE_TITLE = (By.CSS_SELECTOR, 'a> h1')
    POP_UP: tuple[str, str] = (By.CSS_SELECTOR, '[data-a-target="content-classification-gate-overlay-start-watching-button"]')



class TwitchLiveChanelLocatorsMobile:
    LIVE_VIDEO = (By.CSS_SELECTOR, 'video[src^="blob:"]')
    LIVE_CHAT = (By.CSS_SELECTOR, 'div[class*="overlayChatInputBox"]')
    LIVE_VIDEO_ERROR = (By.CSS_SELECTOR, '[data-a-target="player-overlay-content-gate"]')
    POP_UP: tuple[str, str] = (By.CSS_SELECTOR, '[data-a-target="content-classification-gate-overlay-start-watching-button"]')

