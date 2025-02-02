from spoklient.runtime.action_type import ActionType
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.client_request import ClientRequest


class ClientRuntimeContext(object):
    """OData client context"""

    def __init__(self, url, auth_context, proxy={}):
        self.__service_root_url = url
        self.__auth_context = auth_context
        self.__pending_request = None
        self.json_format = None
        self.proxy = proxy

    def authenticate_request(self, request):
        self.__auth_context.authenticate_request(request)

    @property
    def pending_request(self):
        if not self.__pending_request:
            self.__pending_request = ClientRequest(self, self.proxy)
        return self.__pending_request

    def load(self, client_object, properties_to_retrieve=None):
        """Prepare query"""
        if properties_to_retrieve is None:
            properties_to_retrieve = []
        if properties_to_retrieve:
            select_expr = ",".join(properties_to_retrieve)
            client_object = client_object.select(select_expr)
        qry = ClientQuery(client_object.resource_url, ActionType.ReadEntity)
        self.pending_request.add_query(qry, client_object)

    def execute_request_direct(self, request):
        return self.pending_request.execute_request_direct(request)

    def execute_query(self):
        self.pending_request.execute_query()

    def add_query(self, query, result_object=None):
        self.pending_request.add_query(query, result_object)

    @property
    def service_root_url(self):
        return self.__service_root_url

    @service_root_url.setter
    def service_root_url(self, value):
        self.__service_root_url = value

    @property
    def auth_context(self):
        return self.__auth_context
