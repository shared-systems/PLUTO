import requests as req

from json import loads, dumps, JSONDecodeError
from os import path, curdir, remove

from requests.exceptions import ConnectionError


class CredentialManager(object):
    # TODO: Consider using something like marshal, shelve, or pickle
    def __init__(self, file_path="./"):

        self.file_path = file_path
        if not path.exists(path.join(path.abspath(self.file_path), ".credential_store")):
            self.credential_store = path.join(path.abspath(self.file_path), ".credential_store")

            # Create file
            with open(self.credential_store, "w+") as credential_store:
                pass

        else:
            self.credential_store = path.join(path.abspath(self.file_path), ".credential_store")

    def put(self, obj):
        with open(self.credential_store, "w+") as store:
            # store.write(dumps(obj))
            store.write(obj)

    def get(self):
        with open(self.credential_store, "r+") as store:
            # store = loads(store.read())
            return store.read()


class Api(object):
    # Set store path globally
    store_path = path.abspath(curdir)

    def __init__(self, endpoint: str = "/", domain: str = "pacific.cs.pdx.edu", port: int = 8080, auth: bool = False):
  
        self.domain = domain
        self.port = port

        self.endpoint = endpoint
        if not self.endpoint.startswith("/"):
            self.endpoint = f"/{self.endpoint}"

        self.url: str = f"http://{self.domain}:{self.port}/api/v1{self.endpoint}"

        self.auth: bool = auth
        self.token: str = None

    def __enter__(self):
        self.store = CredentialManager(self.store_path)
        self.token = self.store.get()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auth and self.token:
            self.store.put(self.token)

    def get(self):

        headers = {"x-access-token": self.token}
        try:
            res: req.Response = req.get(self.url, headers=headers)
            return res.status_code, res.json()
        except (ConnectionError, JSONDecodeError) as err:
            # log(err)
            return None, None

    def post(self, payload: dict={}):

        headers = {"x-access-token": self.token}
        try:
            res: req.Response = req.post(self.url, payload, headers=headers)
            res_json: dict = res.json()

            if res_json.get('token'):
                self.auth = True
                self.token = res_json.get('token')

            return res.status_code, res_json
        except (ConnectionError, JSONDecodeError) as err:
            # log(err)
            return None, None

    def put(self, payload: dict={}):

        try:
            headers = {"x-access-token": self.token}
            res: req.Response = req.put(self.url, payload, headers=headers)
            return res.status_code, res.json()

        except (ConnectionError, JSONDecodeError) as err:
            # log(err)
            return None, None

    def delete(self):

        try:
            headers = {"x-access-token": self.token}
            res: req.Response = req.delete(self.url, headers=headers)
            return res.status_code, res.json()

        except (ConnectionError, JSONDecodeError) as err:
            # log(err)
            return None, None
