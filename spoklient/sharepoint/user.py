from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.odata.odata_path_parser import ODataPathParser
from spoklient.runtime.resource_path_entity import ResourcePathEntity
from spoklient.sharepoint.principal import Principal


class User(Principal):
    """Represents a user in Microsoft SharePoint Foundation. A user is a type of SP.Principal."""

    @property
    def groups(self):
        """Gets a collection of group objects that represents all of the groups for the user."""
        if self.is_property_available('Groups'):
            return self.properties['Groups']
        else:
            from spoklient.sharepoint.group_collection import GroupCollection
            return GroupCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "Groups"))

    def delete_object(self):
        """Deletes the user."""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
