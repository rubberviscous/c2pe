from googleapiclient.discovery import build

from c2pe.backends import get_credentials
from c2pe.backends.base_backend import BaseBackend


class GoogleBackend(BaseBackend):
    DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

    def __init__(self):
        token_path = "token.json"
        creds = get_credentials(token_path)
        self.service = build('docs', 'v1', credentials=creds)
        document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

    def save(self):
        pass
