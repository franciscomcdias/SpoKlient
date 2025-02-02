from spoklient.runtime.action_type import ActionType
from spoklient.runtime.client_object_collection import ClientObjectCollection
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.resource_path_service_operation import ResourcePathServiceOperation
from spoklient.sharepoint.file import File


class FileCollection(ClientObjectCollection):
    """Represents a collection of File resources."""
    def __init__(self, context, resource_path=None):
        super(FileCollection, self).__init__(context, File, resource_path)

    def add(self, file_creation_information):
        """Creates a File resource"""
        file_new = File(self.context)
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "add",
                                                  {
                                                      "overwrite": file_creation_information.overwrite,
                                                      "url": file_creation_information.url
                                                  },
                                                  file_creation_information.content)
        self.context.add_query(qry, file_new)
        self.add_child(file_new)
        return file_new

    def add_template_file(self, url_of_file, template_file_type):
        """Adds a ghosted file to an existing list or document library."""
        file_new = File(self.context)
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "addTemplateFile",
                                                  {
                                                      "urlOfFile": url_of_file,
                                                      "templateFileType": template_file_type
                                                  })
        self.context.add_query(qry, file_new)
        self.add_child(file_new)
        return file_new

    def get_by_url(self, url):
        """Retrieve File object by url"""
        return File(self.context, ResourcePathServiceOperation(self.context, self.resource_path, "GetByUrl", [url]))
