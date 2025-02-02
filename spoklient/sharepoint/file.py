from spoklient.runtime.action_type import ActionType
from spoklient.runtime.client_object import ClientObject
from spoklient.runtime.client_query import ClientQuery
from spoklient.runtime.client_result import ClientResult
from spoklient.runtime.resource_path_entity import ResourcePathEntity
from spoklient.runtime.resource_path_service_operation import ResourcePathServiceOperation
from spoklient.runtime.utilities.http_method import HttpMethod
from spoklient.runtime.utilities.request_options import RequestOptions
from spoklient.sharepoint.listitem import ListItem
from spoklient.sharepoint.webparts.limited_webpart_manager import LimitedWebPartManager
from spoklient.runtime.odata.odata_path_parser import ODataPathParser


class AbstractFile(ClientObject):
    def read(self, response_object=False):
        """Immediately read content of file"""
        if not self.is_property_available("ServerRelativeUrl"):
            raise ValueError
        response = File.open_binary(
            self.context, self.properties["ServerRelativeUrl"])
        if not response_object:
            return response.content
        return response

    def write(self, content):
        """Immediately writes content of file"""
        if not self.is_property_available("ServerRelativeUrl"):
            raise ValueError
        response = File.save_binary(
            self.context, self.properties["ServerRelativeUrl"], content)
        return response

    def delete_object(self):
        """Deletes the file."""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)


class File(AbstractFile):
    """Represents a file in a SharePoint Web site that can be a Web Part Page, an item in a document library,
    or a file in a folder."""

    def approve(self, comment):
        """Approves the file submitted for content approval with the specified comment."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "approve",
                                                  {
                                                      "comment": comment
                                                  })
        self.context.add_query(qry)

    def deny(self, comment):
        """Denies approval for a file that was submitted for content approval."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "deny",
                                                  {
                                                      "comment": comment
                                                  })
        self.context.add_query(qry)

    def copyto(self, new_relative_url, overwrite):
        """Copies the file to the destination URL."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "moveto",
                                                  {
                                                      "newurl": new_relative_url,
                                                      "boverwrite": overwrite
                                                  },
                                                  None)
        self.context.add_query(qry)

    def moveto(self, new_relative_url, flag):
        """Moves the file to the specified destination URL."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "moveto",
                                                  {
                                                      "newurl": new_relative_url,
                                                      "flags": flag
                                                  },
                                                  None)
        self.context.add_query(qry)

    def publish(self, comment):
        """Submits the file for content approval with the specified comment."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "publish",
                                                  {
                                                      "comment": comment,
                                                  }
                                                  )
        self.context.add_query(qry)

    def unpublish(self, comment):
        """Removes the file from content approval or unpublish a major version."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "unpublish",
                                                  {
                                                      "comment": comment,
                                                  }
                                                  )
        self.context.add_query(qry)

    def checkout(self):
        """Checks out the file from a document library based on the check-out type."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "checkout",
                                                  )
        self.context.add_query(qry)

    def checkin(self, comment, checkin_type):
        """Checks the file in to a document library based on the check-in type."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "checkin",
                                                  {
                                                      "comment": comment,
                                                      "checkInType": checkin_type
                                                  }
                                                  )
        self.context.add_query(qry)

    def undocheckout(self):
        """Reverts an existing checkout for the file."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "undocheckout",
                                                  )
        self.context.add_query(qry)

    def recycle(self):
        """Moves the file to the Recycle Bin and returns the identifier of the new Recycle Bin item."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "recycle",
                                                  )
        self.context.add_query(qry)

    def get_limited_webpart_manager(self, scope):
        """Specifies the control set used to access, modify, or add Web Parts associated with this Web Part Page and
        view. """
        return LimitedWebPartManager(self.context,
                                     ResourcePathServiceOperation(self.context, self.resource_path,
                                                                  "getlimitedwebpartmanager",
                                                                  [scope]
                                                                  ))

    def start_upload(self, upload_id, content):
        """Starts a new chunk upload session and uploads the first fragment."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "startupload",
                                                  {
                                                      "uploadID": upload_id
                                                  },
                                                  content
                                                  )
        result = ClientResult
        self.context.add_query(qry, result)
        return result

    def continue_upload(self, upload_id, file_offset, content):
        """Continues the chunk upload session with an additional fragment. The current file content is not changed."""
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "continueupload",
                                                  {
                                                      "uploadID": upload_id,
                                                      "fileOffset": file_offset,
                                                  },
                                                  content
                                                  )
        result = ClientResult
        self.context.add_query(qry, result)
        return result

    def finish_upload(self, upload_id, file_offset, content):
        """Uploads the last file fragment and commits the file. The current file content is changed when this method
        completes. """
        qry = ClientQuery.service_operation_query(self,
                                                  ActionType.PostMethod,
                                                  "finishupload",
                                                  {
                                                      "uploadID": upload_id,
                                                      "fileOffset": file_offset,
                                                  },
                                                  content
                                                  )
        self.context.add_query(qry, self)
        return self

    @staticmethod
    def save_binary(ctx, server_relative_url, content):
        try:
            from urllib import quote  # Python 2.X
        except ImportError:
            from urllib.parse import quote  # Python 3+
        server_relative_url = quote(server_relative_url)
        url = "{0}web/getfilebyserverrelativeurl('{1}')/\$value".format(
            ctx.service_root_url, server_relative_url)
        request = RequestOptions(url)
        request.method = HttpMethod.Post
        request.set_header('X-HTTP-Method', 'PUT')
        request.data = content
        response = ctx.execute_request_direct(request)
        return response

    @staticmethod
    def open_binary(ctx, server_relative_url):
        try:
            from urllib import quote  # Python 2.X
        except ImportError:
            from urllib.parse import quote  # Python 3+
        server_relative_url = quote(server_relative_url)
        url = "{0}web/getfilebyserverrelativeurl('{1}')/\$value".format(
            ctx.service_root_url, server_relative_url)
        request = RequestOptions(url)
        request.method = HttpMethod.Get
        response = ctx.execute_request_direct(request)
        return response

    @property
    def listitem_allfields(self):
        """Gets a value that specifies the list item field values for the list item corresponding to the file."""
        if self.is_property_available('ListItemAllFields'):
            return self.properties['ListItemAllFields']
        else:
            return ListItem(self.context, ResourcePathEntity(self.context, self.resource_path, "listItemAllFields"))

    @property
    def resource_path(self):
        resource_path = super(File, self).resource_path
        if resource_path:
            return resource_path

        # fallback: create a new resource path
        if self.is_property_available("ServerRelativeUrl"):
            self._resource_path = ResourcePathEntity(
                self.context,
                ResourcePathEntity(self.context, None, "Web"),
                ODataPathParser.from_method("GetFileByServerRelativeUrl",
                                            [self.properties["ServerRelativeUrl"]]))
        elif self.is_property_available("UniqueId"):
            self._resource_path = ResourcePathEntity(
                self.context,
                ResourcePathEntity(self.context, None, "Web"),
                ODataPathParser.from_method("GetFileById",
                                            [{'guid': self.properties["UniqueId"]}]))

        return self._resource_path
