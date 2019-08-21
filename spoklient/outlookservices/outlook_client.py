from spoklient.outlookservices.user import User
from spoklient.runtime.client_runtime_context import ClientRuntimeContext
from spoklient.runtime.odata.v4_json_format import V4JsonFormat
from spoklient.runtime.resource_path_entity import ResourcePathEntity


class OutlookClient(ClientRuntimeContext):
    """Office365 Outlook client context"""

    def __init__(self, ctx_auth):
        self.__service_root_url = "https://outlook.office365.com/api/v1.0/"
        # self.__service_root_url = "https://graph.microsoft.com/v1.0/"
        super(OutlookClient, self).__init__(self.__service_root_url, ctx_auth)
        self.json_format = V4JsonFormat("minimal")

    @property
    def me(self):
        """The Me endpoint is provided as a shortcut for specifying the current user by SMTP address."""
        return User(self, ResourcePathEntity(self, None, "me"))


