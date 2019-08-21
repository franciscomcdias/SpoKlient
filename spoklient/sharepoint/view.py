from spoklient.runtime.client_object import ClientObject
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.resource_path_entity import ResourcePathEntity
from spoklient.sharepoint.view_field_collection import ViewFieldCollection


class View(ClientObject):
    """Specifies a list view."""

    @property
    def view_fields(self):
        if self.is_property_available('ViewFields'):
            return self.properties['ViewFields']
        else:
            return ViewFieldCollection(self.context, ResourcePathEntity(self.context, self.resource_path, "ViewFields"))

    def delete_object(self):
        """The recommended way to delete a view is to send a DELETE request to the View resource endpoint, as shown
        in View request examples."""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
