from spoklient.runtime.action_type import ActionType
from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.resource_path_service_operation import ResourcePathServiceOperation
from spoklient.sharepoint.folder import Folder


class FolderCollection(ClientObjectCollection):
    """Represents a collection of Folder resources."""
    def __init__(self, context, resource_path=None):
        super(FolderCollection, self).__init__(context, Folder, resource_path)

    def add(self, folder_url):
        folder = Folder(self.context)
        folder.set_property("ServerRelativeUrl", folder_url)
        qry = ClientQuery(self.resource_url, ActionType.CreateEntity, folder)
        self.context.add_query(qry, folder)
        return folder

    def get_by_url(self, url):
        """Retrieve Folder resource by url"""
        return Folder(self.context, ResourcePathServiceOperation(self.context, self.resource_path, "GetByUrl", [url]))
