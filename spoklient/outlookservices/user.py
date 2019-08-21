from spoklient.outlookservices.contact_collection import ContactCollection
from spoklient.outlookservices.event_collection import EventCollection
from spoklient.outlookservices.message_collection import MessageCollection
from spoklient.runtime.client_object import ClientObject
from spoklient.runtime.resource_path_entity import ResourcePathEntity


class User(ClientObject):
    """A user in the system."""

    @property
    def contacts(self):
        """Get a contact collection from the default Contacts folder of the signed-in user (.../me/contacts),
        or from the specified contact folder."""
        contacts = ContactCollection(self.context, ResourcePathEntity(self, self._resource_path, "contacts"))
        return contacts

    @property
    def events(self):
        """Get an event collection or an event."""
        events = EventCollection(self.context, ResourcePathEntity(self, self._resource_path, "events"))
        return events

    @property
    def messages(self):
        """Get an event collection or an event."""
        messages = MessageCollection(self.context, ResourcePathEntity(self, self._resource_path, "messages"))
        return messages
