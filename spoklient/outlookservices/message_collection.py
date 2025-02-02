from spoklient.outlookservices.message import Message
from spoklient.runtime.client_object_collection import ClientObjectCollection


class MessageCollection(ClientObjectCollection):
    """Message's collection"""
    def __init__(self, context, resource_path=None):
        super(MessageCollection, self).__init__(context, Message, resource_path)
