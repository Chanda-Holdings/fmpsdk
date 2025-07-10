import json
import logging
from unittest.mock import Mock, patch

import pytest
import requests

import fmpsdk.url_methods as url_methods
from fmpsdk.url_methods import BASE_URL_STABLE, BASE_URL_V4

# Access the private functions before any classes to avoid name mangling
get_base_url_func = url_methods.__get_base_url
return_json_func = url_methods.__return_json
return_binary_stable_func = url_methods.__return_binary_stable


class TestGetBaseUrl:
    """Test the __get_base_url helper function."""

    def test_get_base_url_v4(self):
        """Test getting v4 base URL."""
        result = get_base_url_func("v4")
        assert result == BASE_URL_V4

    def test_get_base_url_stable(self):
        """Test getting stable base URL."""
        result = get_base_url_func("stable")
        assert result == BASE_URL_STABLE

    def test_get_base_url_default(self):
        """Test getting base URL with any other version defaults to stable."""
        result = get_base_url_func("v3")
        assert result == BASE_URL_STABLE

        result = get_base_url_func("unknown")
        assert result == BASE_URL_STABLE


class TestReturnJson:
    """Test the __return_json function."""

    @patch("fmpsdk.url_methods.requests.get")
    def test_successful_json_response(self, mock_get):
        """Test successful JSON response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'[{"symbol": "AAPL", "price": 150.0}]'
        mock_response.json.return_value = [{"symbol": "AAPL", "price": 150.0}]
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        assert result == [{"symbol": "AAPL", "price": 150.0}]
        mock_get.assert_called_once()

    @patch("fmpsdk.url_methods.requests.get")
    def test_premium_endpoint_402_response(self, mock_get):
        """Test premium endpoint 402 status code returns response object."""
        # Mock 402 response (premium endpoint)
        mock_response = Mock()
        mock_response.status_code = 402
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        # Should return the response object for premium detection
        assert result == mock_response

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_json_response(self, mock_get):
        """Test error status code with JSON error response."""
        # Mock 400 response with JSON error
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"Error Message": "Invalid API key"}'
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "invalid"})

        assert isinstance(result, dict)
        assert "Error Message" in result

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_non_json_response(self, mock_get):
        """Test error status code with non-JSON error response."""
        # Mock 500 response with non-JSON error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        assert isinstance(result, dict)
        assert "Error Message" in result
        assert "API request failed with status code 500" in result["Error Message"]

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_unicode_decode_error(self, mock_get):
        """Test error status code with unicode decode error."""
        # Mock response with content that can't be decoded
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = Mock()
        mock_response.content.decode.side_effect = UnicodeDecodeError(
            "utf-8", b"\xff\xfe", 0, 1, "invalid start byte"
        )
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        assert isinstance(result, dict)
        assert "Error Message" in result

    @patch("fmpsdk.url_methods.requests.get")
    def test_csv_response(self, mock_get):
        """Test CSV response parsing."""
        # Mock CSV response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"symbol,price\nAAPL,150.0\nMSFT,300.0"
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test", "datatype": "csv"})

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {"symbol": "AAPL", "price": "150.0"}
        assert result[1] == {"symbol": "MSFT", "price": "300.0"}

    @patch("fmpsdk.url_methods.requests.get")
    def test_csv_response_with_error(self, mock_get):
        """Test CSV response with parsing error."""
        # Mock malformed CSV response - use content that will cause issues
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = (
            b"\xff\xfe"  # Invalid UTF-8 that will cause decode error
        )
        mock_get.return_value = mock_response

        # This should cause a UnicodeDecodeError or similar when trying to decode content
        result = return_json_func("test/path", {"apikey": "test", "datatype": "csv"})

        # Should return None due to exception handling
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_empty_response(self, mock_get):
        """Test empty response returns empty list."""
        # Mock empty response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        assert result == []

    @patch("fmpsdk.url_methods.requests.get")
    def test_empty_dict_response(self, mock_get):
        """Test empty dict response returns empty list."""
        # Mock empty dict response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"{}"
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = return_json_func("test/path", {"apikey": "test"})

        assert result == []

    @patch("fmpsdk.url_methods.requests.get")
    def test_timeout_exception(self, mock_get):
        """Test timeout exception is raised."""
        # Mock timeout exception
        mock_get.side_effect = requests.Timeout("Request timed out")

        with pytest.raises(requests.Timeout):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_connection_error_exception(self, mock_get):
        """Test connection error exception is raised."""
        # Mock connection error
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        with pytest.raises(requests.ConnectionError):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_too_many_redirects_exception(self, mock_get):
        """Test too many redirects exception is raised."""
        # Mock too many redirects error
        mock_get.side_effect = requests.TooManyRedirects("Too many redirects")

        with pytest.raises(requests.TooManyRedirects):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_http_error_exception(self, mock_get):
        """Test HTTP error exception is raised."""
        # Mock HTTP error
        mock_get.side_effect = requests.HTTPError("HTTP error occurred")

        with pytest.raises(requests.HTTPError):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_generic_exception_handling(self, mock_get):
        """Test generic exception handling."""
        # Mock generic exception
        mock_get.side_effect = ValueError("Some other error")

        result = return_json_func("test/path", {"apikey": "test"})

        # Should return None and log error
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_generic_exception_with_response_info(self, mock_get):
        """Test generic exception with response information available."""
        # Mock response object that gets created before exception
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"some content"
        mock_response.text = "some text"

        # Create a side effect that sets response before raising exception
        def side_effect(*args, **kwargs):
            # Simulate that response was created but then an exception occurred
            raise ValueError("Some processing error")

        mock_get.side_effect = side_effect

        result = return_json_func("test/path", {"apikey": "test"})

        # Should return None and log error with response info
        assert result is None

    def test_v4_version_url(self):
        """Test that v4 version uses correct base URL."""
        with patch("fmpsdk.url_methods.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = b"[]"
            mock_response.json.return_value = []
            mock_get.return_value = mock_response

            return_json_func("test/path", {"apikey": "test"}, version="v4")

            # Check that the correct URL was called
            called_url = mock_get.call_args[0][0]
            assert BASE_URL_V4 in called_url


class TestReturnBinaryStable:
    """Test the __return_binary_stable function."""

    @patch("fmpsdk.url_methods.requests.get")
    def test_successful_binary_response(self, mock_get):
        """Test successful binary response."""
        # Mock successful binary response
        mock_response = Mock()
        mock_response.content = b"binary data content"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        assert result == b"binary data content"

    @patch("fmpsdk.url_methods.requests.get")
    def test_empty_binary_response(self, mock_get):
        """Test empty binary response."""
        # Mock empty binary response
        mock_response = Mock()
        mock_response.content = b""
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        assert result == b""

    @patch("fmpsdk.url_methods.requests.get")
    def test_timeout_exception_binary(self, mock_get):
        """Test timeout exception for binary requests."""
        # Mock timeout exception
        mock_get.side_effect = requests.Timeout("Request timed out")

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        # Should return None when exception occurs
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_connection_error_exception_binary(self, mock_get):
        """Test connection error exception for binary requests."""
        # Mock connection error
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        # Should return None when exception occurs
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_too_many_redirects_exception_binary(self, mock_get):
        """Test too many redirects exception for binary requests."""
        # Mock too many redirects error
        mock_get.side_effect = requests.TooManyRedirects("Too many redirects")

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        # Should return None when exception occurs
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_http_error_exception_binary(self, mock_get):
        """Test HTTP error exception for binary requests."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "HTTP error occurred"
        )
        mock_get.return_value = mock_response

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        # Should return None when exception occurs
        assert result is None

    @patch("fmpsdk.url_methods.requests.get")
    def test_generic_exception_binary(self, mock_get):
        """Test generic exception handling for binary requests."""
        # Mock generic exception
        mock_get.side_effect = ValueError("Some other error")

        result = return_binary_stable_func("test/path", {"apikey": "test"})

        # Should return None when exception occurs
        assert result is None


class TestUrlMethodsIntegration:
    """Integration tests to ensure URL methods work together correctly."""

    def test_timeout_values(self):
        """Test that timeout values are properly configured."""
        from fmpsdk.url_methods import CONNECT_TIMEOUT, READ_TIMEOUT

        assert CONNECT_TIMEOUT == 5
        assert READ_TIMEOUT == 30

    def test_logging_configuration(self):
        """Test that logging is properly configured."""
        # Test that requests and urllib3 loggers are set to WARNING level
        requests_logger = logging.getLogger("requests")
        urllib3_logger = logging.getLogger("urllib3")

        assert requests_logger.level == logging.WARNING
        assert urllib3_logger.level == logging.WARNING

    @patch("fmpsdk.url_methods.requests.get")
    def test_url_construction_stable(self, mock_get):
        """Test URL construction for stable API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"[]"
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        return_json_func("company/profile", {"apikey": "test", "symbol": "AAPL"})

        # Verify URL construction
        call_args = mock_get.call_args
        assert call_args[0][0] == f"{BASE_URL_STABLE}company/profile"
        assert call_args[1]["params"] == {"apikey": "test", "symbol": "AAPL"}

    @patch("fmpsdk.url_methods.requests.get")
    def test_url_construction_v4(self, mock_get):
        """Test URL construction for v4 API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"[]"
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        return_json_func("social-sentiments/trending", {"apikey": "test"}, version="v4")

        # Verify URL construction
        call_args = mock_get.call_args
        assert call_args[0][0] == f"{BASE_URL_V4}social-sentiments/trending"

    @patch("fmpsdk.url_methods.requests.get")
    def test_timeout_parameters_passed(self, mock_get):
        """Test that timeout parameters are correctly passed to requests."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"[]"
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        return_json_func("test/path", {"apikey": "test"})

        # Verify timeout parameters
        call_args = mock_get.call_args
        assert call_args[1]["timeout"] == (5, 30)  # (CONNECT_TIMEOUT, READ_TIMEOUT)
