import unittest
from unittest.mock import MagicMock, patch

from hearthstone.assets.fetchcards import hearthstone_api


class TestYourFunctions(unittest.TestCase):

    @patch("requests.post")
    def test_generate_bearer_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mock_token"}
        mock_post.return_value = mock_response

        context = MagicMock()
        client_id = "your_client_id"
        client_secret = "your_client_secret"

        token = hearthstone_api.generate_bearer_token(context, client_id, client_secret)

        self.assertEqual(token, "mock_token")
        context.log.info.assert_called_once_with("generated token is mock_token")

    @patch("requests.post")
    def test_generate_bearer_token_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error message"
        mock_post.return_value = mock_response

        context = MagicMock()
        client_id = "your_client_id"
        client_secret = "your_client_secret"

        token = hearthstone_api.generate_bearer_token(context, client_id, client_secret)

        self.assertIsNone(token)
        context.log.error.assert_called_once_with(
            "failed to generate bearer token due to Error message"
        )

    @patch("requests.get")
    @patch("hearthstone.assets.fetchcards.hearthstone_api.__get_access_token")
    @patch("hearthstone.assets.fetchcards.hearthstone_api.generate_bearer_token")
    def test_get_all_hearthstone_cards_success(
        self, mock_generate_bearer_token, mock_get_access_token, mock_get
    ):
        mock_get_access_token.return_value = ("your_client_id", "your_client_secret")
        mock_generate_bearer_token.return_value = "mock_token"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"mock_data": "mock_value"}
        mock_get.return_value = mock_response

        context = MagicMock()

        result = hearthstone_api.get_all_hearthstone_cards(context)

        self.assertEqual(result, {"mock_data": "mock_value"})
        context.log.info.assert_called_once_with("status code was 200")

    @patch("requests.get")
    @patch("hearthstone.assets.fetchcards.hearthstone_api.__get_access_token")
    @patch("hearthstone.assets.fetchcards.hearthstone_api.generate_bearer_token")
    def test_get_all_hearthstone_cards_failure(
        self, mock_generate_bearer_token, mock_get_access_token, mock_get
    ):
        mock_get_access_token.return_value = ("your_client_id", "your_client_secret")
        mock_generate_bearer_token.return_value = "mock_token"

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        context = MagicMock()

        result = hearthstone_api.get_all_hearthstone_cards(context)

        self.assertIsNone(result)
        context.log.error.assert_called_once_with("Failed to fetch hearthstone cards")


if __name__ == "__main__":
    unittest.main()
