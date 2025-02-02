from spoklient.outlookservices.event import Event
from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.runtime.client_query import ClientQuery


class EventCollection(ClientObjectCollection):
    """Event's collection"""
    def __init__(self, context, resource_path=None):
        super(EventCollection, self).__init__(context, Event, resource_path)

    def add_from_json(self, event_creation_information):
        """Creates a Event resource from JSON"""
        event = Event(self.context)
        qry = ClientQuery.create_entry_query(self, event_creation_information)
        self.context.add_query(qry, event)
        self.add_child(event)
        return event
