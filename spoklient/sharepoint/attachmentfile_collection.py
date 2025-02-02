from spoklient.runtime.action_type import ActionType
from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.resource_path_service_operation import ResourcePathServiceOperation
from spoklient.sharepoint.attachmentfile import Attachmentfile
from spoklient.sharepoint.attachmentfile_creation_information import AttachmentfileCreationInformation
from spoklient.sharepoint.file import File


class AttachmentfileCollection(ClientObjectCollection):
    """Represents a collection of AttachmentFile resources."""
    def __init__(self, context, resource_path=None):
        super(AttachmentfileCollection, self).__init__(context, Attachmentfile, resource_path)

    def add(self, attachment_file_information):
        """Creates an attachment"""
        if isinstance(attachment_file_information, dict):
            attachment_file_information = AttachmentfileCreationInformation(
                attachment_file_information.get('filename'),
                attachment_file_information.get('content')
            )

        file_new = File(self.context)
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "add",
                                                  {
                                                      "filename": attachment_file_information.filename,
                                                  },
                                                  attachment_file_information.content)
        self.context.add_query(qry, file_new)
        self.add_child(file_new)
        return file_new

    def get_by_filename(self, filename):
        """Retrieve Attachmentfile object by filename"""
        return Attachmentfile(self.context,
                              ResourcePathServiceOperation(self.context, self.resource_path, "GetByFileName",
                                                           [filename]))
