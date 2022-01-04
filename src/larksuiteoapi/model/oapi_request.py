# -*- coding: UTF-8 -*-


from typing import Dict, List, Union

from .oapi_header import OapiHeader


class OapiRequest(object):
    def __init__(self, uri='', body=b'', header=None):
        # type: (str, bytes, Union[Dict[str, Union[str, List[str]]], OapiHeader, None]) -> None
        self.uri = uri
        self.body = body

        if header is None:
            header = {}

        self.header = OapiHeader(data=header) if isinstance(header, dict) else header
