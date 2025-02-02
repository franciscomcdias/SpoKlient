import requests
from spoklient.runtime.client_runtime_context import ClientRuntimeContext
from spoklient.runtime.context_web_information import ContextWebInformation
from spoklient.runtime.odata.json_light_format import JsonLightFormat
from spoklient.runtime.odata.odata_metadata_level import ODataMetadataLevel
from spoklient.runtime.utilities.request_options import RequestOptions
from spoklient.sharepoint.site import Site
from spoklient.sharepoint.web import Web


class ClientContext(ClientRuntimeContext):
    """SharePoint client context"""

    def __init__(self, base_url, auth_context, proxy={}):
        if base_url.endswith("/"):
            base_url = base_url[:len(base_url) - 1]
        super(ClientContext, self).__init__(base_url + "/_api/", auth_context, proxy)
        self.__web = None
        self.__site = None
        self.contextWebInformation = None
        self.json_format = JsonLightFormat(ODataMetadataLevel.Verbose)
        self.proxy = proxy

    def ensure_form_digest(self, request_options):
        if not self.contextWebInformation:
            self.request_form_digest()
        request_options.set_header('X-RequestDigest', self.contextWebInformation.form_digest_value)

    def request_form_digest(self):
        """Request Form Digest"""
        request = RequestOptions(self.service_root_url + "contextinfo")
        self.authenticate_request(request)
        request.set_headers(self.json_format.build_http_headers())
        response = requests.post(url=request.url,
                                 headers=request.headers,
                                 auth=request.auth,
                                 proxies=self.proxy)
        self.pending_request.validate_response(response)
        payload = response.json()
        if self.json_format.metadata == ODataMetadataLevel.Verbose:
            payload = payload['d']['GetContextWebInformation']
        self.contextWebInformation = ContextWebInformation()
        self.contextWebInformation.from_json(payload)

    @property
    def web(self):
        """Get Web client object"""
        if not self.__web:
            self.__web = Web(self)
        return self.__web

    @property
    def site(self):
        """Get Site client object"""
        if not self.__site:
            self.__site = Site(self)
        return self.__site
