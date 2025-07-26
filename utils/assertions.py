
class Assertions:
    @staticmethod
    def assert_status_code(response, expected_status_code):
        """Asserts that the response status code matches the expected status code."""
        assert response.status_code == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status_code}. Response: {response.text}"

    @staticmethod
    def assert_json_field(response, field_name, expected_value=None):
        """Asserts that a JSON field exists and optionally matches an expected value."""
        try:
            json_data = response.json()
            assert field_name in json_data, \
                f"Expected field \'{field_name}\' not found in response. Response: {response.text}"
            if expected_value is not None:
                assert json_data[field_name] == expected_value, \
                    f"Expected field \'{field_name}\' to be \'{expected_value}\', but got \'{json_data[field_name]}\'. Response: {response.text}"
        except ValueError:
            assert False, f"Response is not valid JSON. Response: {response.text}"

    @staticmethod
    def assert_response_time_less_than(response, max_response_time_ms):
        """Asserts that the response time is less than the specified maximum."""
        assert response.elapsed.total_seconds() * 1000 < max_response_time_ms, \
            f"Response time {response.elapsed.total_seconds() * 1000:.2f}ms exceeded {max_response_time_ms}ms."

    # Add more assertion methods as needed


