"""
Copyright 2018 PeopleDoc
Written by Yann Lachiver
           Joachim Jablon
           Jacques Rott

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Iterable
from urllib.parse import urljoin

import requests

from vault_cli import sessions, types
from vault_cli.client import VaultAPIException, VaultClientBase


class RequestsVaultClient(VaultClientBase):
    def _init_session(self, url: str, verify: types.VerifyOrCABundle) -> None:
        self.session = self.create_session(verify)

        self.url = urljoin(url, "v1/")

    def _full_url(self, path: str) -> str:
        url = urljoin(self.url, self.base_path)
        return urljoin(url, path)

    @staticmethod
    def handle_error(
        response: requests.Response, expected_code: int = requests.codes.ok
    ):
        if response.status_code != expected_code:
            raise VaultAPIException(response.status_code, response.text)

    @staticmethod
    def create_session(verify: types.VerifyOrCABundle) -> requests.Session:
        session = sessions.Session()
        session.verify = verify
        return session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_type, exc_value, traceback)

    def _authenticate_token(self, token: str) -> None:
        self.session.headers.update({"X-Vault-Token": token})

    def _authenticate_userpass(self, username: str, password: str) -> None:
        data = {"password": password}
        response = self.session.post(
            self.url + "auth/userpass/login/" + username, json=data, headers={}
        )
        self.handle_error(response)

        json_response = response.json()
        self.session.headers.update(
            {"X-Vault-Token": json_response.get("auth").get("client_token")}
        )

    def _get_secret_and_metadata(self, path: str) -> types.JSONDict:
        url = self._full_url(path)
        response = self.session.get(url)
        self.handle_error(response)
        json_response = response.json()
        return json_response["data"]

    def get_secret(self, path: str) -> types.JSONValue:
        data = self._get_secret_and_metadata(path)
        return data["value"]

    def list_secrets(self, path: str) -> Iterable[str]:
        url = self._full_url(path).rstrip("/")
        response = self.session.get(url, params={"list": "true"})
        try:
            self.handle_error(response)
        except VaultAPIException as exc:
            if exc.status_code == 404:
                return []
            raise
        json_response = response.json()
        return json_response["data"]["keys"]

    def set_secret(self, path: str, value: types.JSONValue) -> None:
        url = self._full_url(path)
        response = self.session.put(url, json={"value": value})
        self.handle_error(response, requests.codes.no_content)

    def delete_secret(self, path: str) -> None:
        url = self._full_url(path)
        response = self.session.delete(url)
        self.handle_error(response, requests.codes.no_content)
