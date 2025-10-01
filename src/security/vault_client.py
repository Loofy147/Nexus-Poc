import os
import hvac
from typing import Dict, Optional


class VaultClient:
    """
    A client for interacting with HashiCorp Vault to manage secrets.
    This client is designed to be reusable across different services.
    """

    def __init__(self):
        """
        Initializes the Vault client using environment variables for configuration.
        - VAULT_ADDR: The address of the Vault server.
        - VAULT_TOKEN: The token for authenticating with Vault.
        """
        self.vault_addr = os.getenv('VAULT_ADDR')
        self.vault_token = os.getenv('VAULT_TOKEN')

        if not self.vault_addr or not self.vault_token:
            raise ValueError("VAULT_ADDR and VAULT_TOKEN environment variables must be set.")

        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token
        )
        print("VaultClient: Initialized and authenticated.")

    def get_secret(self, path: str, mount_point: str = 'nexus') -> Optional[Dict]:
        """
        Retrieves a secret from Vault's Key-Value v2 secrets engine.

        :param path: The path to the secret.
        :param mount_point: The mount point of the KV secrets engine.
        :return: A dictionary containing the secret data, or None if an error occurs.
        """
        try:
            print(f"VaultClient: Attempting to read secret from path: '{mount_point}/{path}'")
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=mount_point,
            )

            secret_data = response['data']['data']
            print(f"VaultClient: Successfully retrieved secret from path: '{mount_point}/{path}'")
            return secret_data

        except hvac.exceptions.InvalidPath:
            print(f"VaultClient: ERROR - The secret path '{mount_point}/{path}' was not found.")
            return None
        except hvac.exceptions.Forbidden:
            print(f"VaultClient: ERROR - Permission denied. Check Vault policies for token.")
            return None
        except Exception as e:
            print(f"VaultClient: ERROR - An unexpected error occurred: {e}")
            return None