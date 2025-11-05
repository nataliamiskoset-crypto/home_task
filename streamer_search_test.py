import allure
import pytest

from assertpy import assert_that

from tests.ui.base_test import BaseTest

class TestStreamers(BaseTest):
    SEARCH_CASES = [
        ("starcraft ii", 2, 4)
    ]

    @pytest.mark.parametrize(
        "query,result_index,live_index",
        SEARCH_CASES,
        ids=[f'query="{q}"-res#{ri}-live#{li}' for q, ri, li in SEARCH_CASES],
    )
    @allure.description("Search for streamer and open a live channel; verify channel title")
    @allure.title("Search & Open Live Channel")
    @pytest.mark.run(order=1)
    def test_search_streamer(self, query: str, result_index: int, live_index: int) -> None:
        self.twitch_home_page.search_by_text(query).select_resources_by_index(result_index)
        selected_live_chanel = self.twitch_search_result_page.select_live_channel_by_index(live_index)
        self.twitch_live_chanel_page.verify_channel_is_live()
        assert_that(
            selected_live_chanel.strip().lower()
        ).described_as("Success message after password reset").is_equal_to(
            self.twitch_live_chanel_page.get_channel_title().strip().lower()
        )
        self.twitch_live_chanel_page.take_screenshot()

