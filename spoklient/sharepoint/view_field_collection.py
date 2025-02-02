from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.sharepoint.field import Field


class ViewFieldCollection(ClientObjectCollection):
    """Represents a collection of Field resources."""
    def __init__(self, context, resource_path=None):
        super(ViewFieldCollection, self).__init__(context, Field, resource_path)

    def map_json(self, payload):
        super(ViewFieldCollection, self).map_json(payload)
