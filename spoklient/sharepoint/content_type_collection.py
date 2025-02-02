from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.sharepoint.content_type import ContentType


class ContentTypeCollection(ClientObjectCollection):
    """Content Type resource collection"""
    def __init__(self, context, resource_path=None):
        super(ContentTypeCollection, self).__init__(context, ContentType, resource_path)

