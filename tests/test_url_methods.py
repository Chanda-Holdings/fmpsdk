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
        # Test v3 specifically (now supported)
        result = get_base_url_func("v3")
        assert result == "https://financialmodelingprep.com/api/v3/"

        # Test unsupported version defaults to stable
        result = get_base_url_func("v5")
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

        assert len(result) > 0 and result[0].get("symbol", "") != ""
        mock_get.assert_called_once()

    @patch("fmpsdk.url_methods.requests.get")
    def test_premium_endpoint_402_response(self, mock_get):
        """Test premium endpoint 402 status code raises PremiumEndpointException."""
        from fmpsdk.exceptions import PremiumEndpointException

        # Mock 402 response (premium endpoint)
        mock_response = Mock()
        mock_response.status_code = 402
        mock_response.text = "Premium Endpoint. Please upgrade your subscription."
        mock_response.content = b'{"Error Message": "Premium Endpoint"}'
        mock_get.return_value = mock_response

        with pytest.raises(PremiumEndpointException):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_json_response(self, mock_get):
        """Test error status code with JSON error response raises Exception."""
        # Mock 404 response with JSON error (404 is not in retryable codes)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b'{"Error Message": "Invalid API key"}'
        mock_response.text = '{"Error Message": "Invalid API key"}'
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Resource not found. Status code: 404"):
            return_json_func("test/path", {"apikey": "invalid"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_non_json_response(self, mock_get):
        """Test error status code with non-JSON error response raises Exception."""
        # Mock 404 response with non-JSON error (404 is not in retryable codes)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b"Not Found"
        mock_response.text = "Not Found"
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match=r"Resource not found. Status code: 404"):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_error_status_code_with_unicode_decode_error(self, mock_get):
        """Test error status code with unicode decode error raises Exception."""
        # Mock response with content that can't be decoded
        mock_response = Mock()
        mock_response.status_code = 404  # Use non-retryable status
        mock_response.reason = "Not Found"
        mock_response.content = Mock()
        mock_response.content.decode.side_effect = UnicodeDecodeError(
            "utf-8", b"\xff\xfe", 0, 1, "invalid start byte"
        )
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match=r"Resource not found. Status code: 404"):
            return_json_func("test/path", {"apikey": "test"})

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
        assert len(result) > 0 and result[0].get("symbol", "") != ""
        assert len(result) > 0 and result[0].get("symbol", "") != ""

    @patch("fmpsdk.url_methods.requests.get")
    def test_csv_response_with_error(self, mock_get):
        """Test CSV response with decode error raises UnicodeDecodeError."""
        # Mock response with invalid UTF-8 content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = (
            b"\xff\xfe"  # Invalid UTF-8 that will cause decode error
        )
        mock_get.return_value = mock_response

        # This should cause a UnicodeDecodeError when trying to decode content
        with pytest.raises(UnicodeDecodeError):
            return_json_func("test/path", {"apikey": "test", "datatype": "csv"})

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
        """Test generic exception handling raises the exception."""
        # Mock generic exception
        mock_get.side_effect = ValueError("Some other error")

        with pytest.raises(ValueError, match="Some other error"):
            return_json_func("test/path", {"apikey": "test"})

    @patch("fmpsdk.url_methods.requests.get")
    def test_generic_exception_with_response_info(self, mock_get):
        """Test generic exception with response information available raises the exception."""

        # Create a side effect that raises exception
        def side_effect(*args, **kwargs):
            # Simulate that an exception occurred during processing
            raise ValueError("Some processing error")

        mock_get.side_effect = side_effect

        with pytest.raises(ValueError, match="Some processing error"):
            return_json_func("test/path", {"apikey": "test"})

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

        result = return_json_func(
            "company/profile", {"apikey": "test", "symbol": "AAPL"}
        )

        # Verify URL construction
        call_args = mock_get.call_args
        assert call_args[0][0] == f"{BASE_URL_STABLE}company/profile"
        # Verify the function returns the expected result
        assert result == []

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


class TestUrlMethodsCoverageCompleteness:
    """Tests to achieve 100% coverage for remaining uncovered lines in url_methods.py."""

    @patch("fmpsdk.url_methods.requests.get")
    @patch("fmpsdk.url_methods.time.sleep")
    def test_rate_limit_retry_with_logging(self, mock_sleep, mock_get):
        """Test rate limit retry logic with logging (covers lines 67-77)."""
        # Mock rate limit response on first call, success on second
        rate_limit_response = Mock()
        rate_limit_response.status_code = 429  # RATE_LIMIT_STATUS_CODE
        rate_limit_response.text = "Rate limit exceeded"

        success_response = Mock()
        success_response.status_code = 200
        success_response.content = b'{"data": "success"}'
        success_response.json.return_value = {"data": "success"}

        mock_get.side_effect = [rate_limit_response, success_response]

        # Capture logging output
        with patch("fmpsdk.url_methods.logging") as mock_logging:
            result = return_json_func(
                "test/path", {"apikey": "test"}, retries=1, retry_delay=0.1
            )

            # Verify logging calls
            mock_logging.warning.assert_called_once()
            mock_logging.info.assert_called_once()

            # Verify sleep was called with retry delay
            mock_sleep.assert_called_once_with(0.1)

            # Verify successful result
            assert result == {"data": "success"}

    @patch("fmpsdk.url_methods.requests.get")
    def test_csv_parsing_error_handling(self, mock_get):
        """Test CSV parsing error handling (covers lines 90-92)."""
        import csv

        # Mock response with valid content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"valid csv content"

        mock_get.return_value = mock_response

        # Mock the CSV processing to raise csv.Error
        with patch("fmpsdk.url_methods.csv.DictReader") as mock_reader:
            mock_reader.side_effect = csv.Error("Invalid CSV format")

            with patch("fmpsdk.url_methods.logging") as mock_logging:
                with pytest.raises(csv.Error, match="Invalid CSV format"):
                    # Use datatype=csv to trigger CSV processing path
                    return_json_func("test/path", {"apikey": "test", "datatype": "csv"})

                # Verify error logging occurred (might be called multiple times due to error handling)
                assert mock_logging.error.call_count >= 1

    @patch("fmpsdk.url_methods.requests.get")
    @patch("fmpsdk.url_methods.time.sleep")
    def test_read_timeout_retry_logic(self, mock_sleep, mock_get):
        """Test read timeout retry logic (covers lines 104-110)."""
        # Mock ReadTimeout on first call, success on second
        success_response = Mock()
        success_response.status_code = 200
        success_response.content = b'{"data": "success"}'
        success_response.json.return_value = {"data": "success"}

        mock_get.side_effect = [
            requests.exceptions.ReadTimeout("Read timeout"),
            success_response,
        ]

        with patch("fmpsdk.url_methods.logging") as mock_logging:
            result = return_json_func(
                "test/path", {"apikey": "test"}, retries=1, retry_delay=0.1
            )

            # Verify logging calls
            mock_logging.error.assert_called_once()
            mock_logging.info.assert_called_once()

            # Verify sleep was called
            mock_sleep.assert_called_once_with(0.1)

            # Verify successful result
            assert result == {"data": "success"}

    @patch("fmpsdk.url_methods.requests.get")
    def test_read_timeout_no_retries_left(self, mock_get):
        """Test read timeout with no retries raises exception (covers lines 105-106)."""
        mock_get.side_effect = requests.exceptions.ReadTimeout("Read timeout")

        with pytest.raises(requests.exceptions.ReadTimeout):
            return_json_func("test/path", {"apikey": "test"}, retries=0)

    @patch("fmpsdk.url_methods.requests.get")
    def test_json_decode_error_re_raised(self, mock_get):
        """Test JSON decode error is re-raised (covers line 132)."""
        # Mock response with invalid JSON
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"invalid json content"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        mock_get.return_value = mock_response

        with pytest.raises(json.JSONDecodeError):
            return_json_func("test/path", {"apikey": "test"})
