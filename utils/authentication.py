
class Auth:
    @staticmethod
    def get_api_key_header(api_key):
        """Returns a dictionary for API key authentication header."""
        return {"X-API-Key": api_key}

    @staticmethod
    def get_bearer_token_header(token):
        """Returns a dictionary for Bearer token authentication header."""
        return {"Authorization": f"Bearer {token}"}

    # Add more authentication methods as needed (e.g., OAuth, Basic Auth)


