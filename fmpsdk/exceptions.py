RETRYABLE_STATUS_CODE = 429
INVALID_API_KEY_STATUS_CODE = 401
PREMIUM_STATUS_CODE = 402
SUCCESS_STATUS_CODE = 200
POSSIBLE_INVALID_EXCHANGE_CODE = 400


class PremiumEndpointException(Exception):
    pass


class RateLimitExceededException(Exception):
    pass


class InvalidQueryParameterException(Exception):
    pass


class InvalidAPIKeyException(Exception):
    pass


class InvalidExchangeCodeException(Exception):
    pass
