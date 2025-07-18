

RETRYABLE_STATUS_CODES = {429}
INVALID_API_KEY_STATUS_CODES = {401}
PREMIUM_STATUS_CODES = {402}
SUCCESS_STATUS_CODES = {200}


class PremiumEndpointException(Exception):
    pass


class RateLimitExceededException(Exception):
    pass


class InvalidQueryParameterException(Exception):
    pass


class InvalidAPIKeyException(Exception):
    pass