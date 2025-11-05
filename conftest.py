# tests/conftest.py
import os
import base64
import logging
from contextlib import suppress
from _pytest.nodes import Item

from typing import Optional, Generator

import pytest
from _pytest.config.argparsing import Parser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from enums.drivers_type import DriversType  # np. Enum: CHROME, CHROME_HEADLESS, FIREFOX, REMOTE


# -----------------------------
# Opcje CLI / ini
# -----------------------------
def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--driver",
        action="store",
        choices=[d.value for d in DriversType],
        default="chrome",
        help="Browser: chrome | chrome_headless | firefox | remote",
    )
    parser.addoption(
        "--device",
        action="store",
        default=None,  # brak emulacji gdy None
        help="Chrome mobile emulation deviceName (e.g. 'Pixel 7', 'iPhone SE')",
    )
    parser.addoption(
        "--grid-url",
        action="store",
        default=os.getenv("SELENIUM_GRID_URL", "http://localhost:4444/wd/hub"),
        help="Selenium Grid URL for --driver=remote",
    )
    parser.addoption(
        "--wait-timeout",
        action="store",
        type=int,
        default=10,
        help="Explicit wait timeout (seconds)",
    )

def _get_base_url(item: Item) -> str:
    with suppress(Exception):
        url = item.config.getoption("--base-url")
        if url:
            return url.rstrip("/")
    with suppress(Exception):
        ini_val = item.config.getini("base_url")
        if ini_val:
            return str(ini_val).rstrip("/")
    return (os.getenv("BASE_URL") or "https://www.twitch.tv/").rstrip("/")


def _build_chrome_options(headless: bool, device: Optional[str]) -> webdriver.ChromeOptions:
    opts = webdriver.ChromeOptions()
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False,
        },
    )
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-search-engine-choice-screen")
    opts.add_argument(
        "--disable-features=IsolateOrigins,site-per-process,VizDisplayCompositor,"
        "SidePanelPinning,OptimizationGuideModelDownloading,OptimizationHintsFetching,"
        "OptimizationTargetPrediction,OptimizationHints"
    )

    if headless:
        opts.add_argument("--headless=new")

    if device:
        opts.add_experimental_option("mobileEmulation", {"deviceName": device})
    else:
        opts.add_argument("--start-maximized")

    return opts


def pytest_runtest_setup(item: Item) -> None:
    if not hasattr(item, "cls"):
        return

    driver_name: str = item.config.getoption("--driver")
    device: Optional[str] = item.config.getoption("--device")
    grid_url: str = item.config.getoption("--grid-url")
    wait_timeout: int = int(item.config.getoption("--wait-timeout"))
    base_url: str = _get_base_url(item)

    if driver_name in ("chrome", "chrome_headless"):
        headless = (driver_name == "chrome_headless")
        options = _build_chrome_options(headless=headless, device=device)
        driver = webdriver.Chrome(options=options)

    elif driver_name == "firefox":
        ff_opts = webdriver.FirefoxOptions()
        if driver_name == "firefox" and device:
            pytest.skip("🚫📱  Mobile emulation is not supported in Firefox. "
                        "Use Chrome (e.g. --driver=chrome) or remove --device.")
            pass
        driver = webdriver.Firefox(options=ff_opts)
        if not device:
            with suppress(Exception):
                driver.maximize_window()

    elif driver_name == "remote":
        options = _build_chrome_options(headless=False, device=device)
        driver = webdriver.Remote(command_executor=grid_url, options=options)
        if not device:
            with suppress(Exception):
                driver.maximize_window()

    else:
        raise ValueError(f"Unsupported driver: {driver_name}")

    driver.get(base_url)
    wait = WebDriverWait(driver, wait_timeout)

    item.cls.driver = driver
    item.cls.wait = wait
    item.cls.emulator = bool(device)

    setattr(item, "_driver_created", True)


def pytest_runtest_teardown(item: Item, nextitem) -> None:
    if hasattr(item, "_driver_created") and getattr(item, "_driver_created"):
        with suppress(Exception):
            drv = getattr(item.cls, "driver", None)
            if drv:
                drv.quit()
        for attr in ("driver", "wait", "emulator"):
            with suppress(Exception):
                if hasattr(item.cls, attr):
                    delattr(item.cls, attr)
