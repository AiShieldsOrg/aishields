import pytest
from sensitive_info_disclosure.sensitive_data_sanitizer import SensitiveDataSanitizer
from sensitive_info_disclosure.config import SENSITIVE_DATA_CONFIGS

test_cases = {
    "CREDIT_CARD": "4012-8888-8888-8881",
    "EMAIL": "john.doe@example.com",
    "IBAN_CODE": "DE89370400440532013000",
    "IP_ADDRESS": "192.168.0.1",
    "PHONE_NUMBER": "555-123-4567",
    "US_SSN": "123-45-6789",
    "UUID": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
    "US_DRIVING_LICENSE": "CA1234567",
    "US_BANK_ACCOUNT": "123456789",
}


@pytest.fixture
def sensitive_data_sanitizer():
    return SensitiveDataSanitizer()


def test_sanitize_input(sensitive_data_sanitizer):
    for entity, input_content in test_cases.items():
        input_prompt = f"Test {entity} with {input_content}"
        placeholder = SENSITIVE_DATA_CONFIGS[entity]["placeholder"]
        sanitized_input = sensitive_data_sanitizer.sanitize_input(input_prompt)
        assert placeholder in sanitized_input, f"Failed to sanitize {entity} in {input_prompt}"
