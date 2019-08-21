from spoklient.onedrive.drive import Drive
from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.runtime.resource_path_entity import ResourcePathEntity


class DriveCollection(ClientObjectCollection):
    """Drive's collection"""

    def __init__(self, context, resource_path=None):
        super(DriveCollection, self).__init__(context, Drive, resource_path)

    def get_by_id(self, drive_id):
        """Retrieve Drive by unique identifier"""
        return Drive(self.context,
                     ResourcePathEntity(self.context, self.resource_path, drive_id))
