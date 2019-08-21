from spoklient.runtime.client_object import ClientObject
from spoklient.runtime.resource_path_entity import ResourcePathEntity
from spoklient.sharepoint.web import Web

class Site(ClientObject):
    """Site client object"""

    def __init__(self, context):
        super(Site, self).__init__(context, ResourcePathEntity(context, None, "Site"))

    @property
    def root_web(self):
        """Get root web"""
        if self.is_property_available('RootWeb'):
            return self.properties['RootWeb']
        else:
            return Web(self.context, ResourcePathEntity(self.context, self.resource_path, "RootWeb"))
