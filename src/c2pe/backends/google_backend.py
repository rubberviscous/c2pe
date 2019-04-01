import os
from typing import List, Tuple

from googleapiclient.discovery import build

from c2pe.backends.google.authentication.utils import get_credentials
from c2pe.backends.base_backend import BaseBackend


class GoogleBackend(BaseBackend):
    DOCUMENT_ID = '1QkTyeO_y9-2kFdBy8jbvSTTaMvMSaEl-ecgfka4IPHE'
    # DOC_BODY = {
    #         'title': title,
    #         'content': [
    #             {
    #                 'endIndex': 1,
    #                 'sectionBreak': {
    #                     'sectionStyle': {
    #                         'columnSeparatorStyle': 'NONE',
    #                         'contentDirection': 'LEFT_TO_RIGHT'
    #                     }
    #                 }
    #             }
    #         ]
    # }

    def __init__(self, data: List[Tuple], *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        token_path = f'/Users/michaelxue/Projects/c2pe/src/tests/token.json'
        creds = get_credentials(token_path)

        self.service = build('docs', 'v1', credentials=creds)
        # document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

        # print(document)

    def save(self):
        title = self.filename[0]
        body = {
            'title': title
        }
        # first create the document with title only
        doc = self.service.documents().create(body=body).execute()
        doc_id = doc.get('documentId')

        # then add the body content

        body = {
            'title': title,
            'content': [
                {
                    'endIndex': 1,
                    'sectionBreak': {
                        'sectionStyle': {
                            'columnSeparatorStyle': 'NONE',
                            'contentDirection': 'LEFT_TO_RIGHT'
                        }
                    }
                }
            ]
        }

        requests = []
        idx = 1
        for line in self.data:
            for sub_line in line:

                sub_line += '\n'
                end_index = len(sub_line)

                row = self.create_row(idx=idx, line=sub_line)
                requests.append(row)

                idx += end_index

            # add extra newline
            newline = '\n'
            row = self.create_row(idx=idx, line=newline)
            requests.append(row)
            idx += len(newline)

        result = self.service.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()

        print('Created document with title: {0}'.format(
            doc.get('title')))

    def create_row(self, **kwargs):
        idx = kwargs.get('idx')
        # end_index = kwargs.get('end_index')
        line = kwargs.get('line')

        row = {
            'insertText': {
                'location': {
                    'index': idx,
                },
                'text': line
            }
        }
        return row

    def output(self):
        pass
