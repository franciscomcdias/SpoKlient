from spoklient.sharepoint.file import AbstractFile
from spoklient.runtime.odata.odata_path_parser import ODataPathParser
from spoklient.runtime.resource_path_entity import ResourcePathEntity


class Attachmentfile(AbstractFile):
    """Represents an attachment file in a SharePoint List Item."""

    @property
    def resource_path(self):
        resource_path = super(Attachmentfile, self).resource_path
        if resource_path:
            return resource_path

        # fallback: create a new resource path
        if self.is_property_available("ServerRelativeUrl"):
            self._resource_path = ResourcePathEntity(
                self.context,
                ResourcePathEntity(self.context, None, "Web"),
                ODataPathParser.from_method("GetFileByServerRelativeUrl",
                                            [self.properties["ServerRelativeUrl"]]))

        return self._resource_path

