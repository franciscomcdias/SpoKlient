from spoklient.runtime.action_type import ActionType
from spoklient.runtime.resource_path_service_operation import ResourcePathServiceOperation
from spoklient.sharepoint.file import File
from spoklient.sharepoint.folder import Folder
from spoklient.sharepoint.folder_collection import FolderCollection
from spoklient.sharepoint.securable_object import SecurableObject
from spoklient.sharepoint.user import User
from spoklient.sharepoint.user_collection import UserCollection
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.resource_path_entity import ResourcePathEntity
from spoklient.sharepoint.group_collection import GroupCollection
from spoklient.sharepoint.list_collection import ListCollection


class Web(SecurableObject):
    """Represents a SharePoint site. A site is a type of SP.SecurableObject.
    Refer this link https://msdn.microsoft.com/en-us/library/office/dn499819.aspx for a details"""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePathEntity(context, None, "Web")
        super(Web, self).__init__(context, resource_path)
        self._web_path = None

    def update(self):
        """Update a Web resource"""
        qry = ClientQuery.update_entry_query(self)
        self.context.add_query(qry)

    def delete_object(self):
        """Delete a Web resource"""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)
        # self.removeFromParentCollection()

    def get_file_by_server_relative_url(self, url):
        """Returns the file object located at the specified server-relative URL."""
        file_obj = File(
            self.context,
            ResourcePathServiceOperation(self.context, self.resource_path, "getfilebyserverrelativeurl", [url])
        )
        return file_obj

    def get_folder_by_server_relative_url(self, url):
        """Returns the folder object located at the specified server-relative URL."""
        folder_obj = Folder(
            self.context,
            ResourcePathServiceOperation(self.context, self.resource_path, "getfolderbyserverrelativeurl", [url])
        )
        return folder_obj

    def ensure_user(self, login_name):
        user = User(self.context)
        qry = ClientQuery.service_operation_query(self, ActionType.PostMethod, "ensureuser", [login_name])
        self.context.add_query(qry, user)
        return user

    @property
    def webs(self):
        """Get child webs"""
        if self.is_property_available('Webs'):
            return self.properties['Webs']
        else:
            from spoklient.sharepoint.web_collection import WebCollection
            parent_web_url = None
            if self.is_property_available('Url'):
                parent_web_url = self.properties['Url']
            return WebCollection(self.context,
                                 ResourcePathEntity(self.context, self.resource_path, "webs"),
                                 parent_web_url)

    @property
    def folders(self):
        """Get folder resources"""
        if self.is_property_available('Folders'):
            return self.properties['Folders']
        else:
            return FolderCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "folders"))

    @property
    def lists(self):
        """Get web list collection"""
        if self.is_property_available('Lists'):
            return self.properties['Lists']
        else:
            return ListCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "lists"))

    @property
    def site_users(self):
        """Get site users"""
        if self.is_property_available('SiteUsers'):
            return self.properties['SiteUsers']
        else:
            return UserCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "siteusers"))

    @property
    def site_groups(self):
        """Gets the collection of groups for the site collection."""
        if self.is_property_available('SiteGroups'):
            return self.properties['SiteGroups']
        else:
            return GroupCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "sitegroups"))

    @property
    def current_user(self):
        """Gets the current user."""
        if self.is_property_available('CurrentUser'):
            return self.properties['CurrentUser']
        else:
            return User(self.context, ResourcePathEntity(self.context, self.resource_path, "CurrentUser"))

    @property
    def parent_web(self):
        """Gets the parent website of the specified website."""
        if self.is_property_available('ParentWeb'):
            return self.properties['ParentWeb']
        else:
            return User(self.context, ResourcePathEntity(self.context, self.resource_path, "ParentWeb"))

    @property
    def service_root_url(self):
        orig_root_url = super(Web, self).service_root_url
        if self.is_property_available("Url"):
            cur_root_url = self.properties["Url"] + "/_api/"
            return cur_root_url
        return orig_root_url
