from spoklient.runtime.auth.authentication_context import AuthenticationContext
from spoklient.runtime.client_request_exception import ClientRequestException
from spoklient.sharepoint.client_context import ClientContext
from spoklient.sharepoint.file import File


class Klient:

    def __init__(self, proxy):
        self.proxy = proxy
        self.context = None

    def connect(self, _url, _id, _secret):
        """
        Authenticates to the remote SPO repository and creates a context
        :param _url:
        :param _id:
        :param _secret:
        :return:
        """
        _auth_context = AuthenticationContext(_url, self.proxy)
        if _auth_context.acquire_token_for_app(_id, _secret):
            self.context = ClientContext(_url, _auth_context, self.proxy)
            self.context.load(self.context.web)
            self.context.execute_query()
        else:
            raise Exception("Could not authenticate")

    def list_titles(self):
        """
        List all the titles from the root of the SPO repository
        :return:
        """
        try:
            titles = self.context.web.lists
            self.context.load(titles)
            self.context.execute_query()
            for item in titles:
                yield item
        except ClientRequestException:
            pass

    def get_title_folder(self, title):
        """
        Get the root folder for a title
        :param title:
        :return:
        """
        list_obj = self.context.web.lists.get_by_title(title)
        folder = list_obj.root_folder
        self.context.load(folder)
        self.context.execute_query()
        return folder

    def list_folders(self, folder):
        """
        List all the folders inside a folder
        :param folder:
        :return:
        """
        sub_folders = folder.folders
        self.context.load(sub_folders)
        self.context.execute_query()
        for cur_folder in sub_folders:
            yield cur_folder, cur_folder.properties["ServerRelativeUrl"]

    def list_files(self, folder, filter_extensions=None):
        """
        List all the files inside a folder
        :param folder:
        :param filter_extensions:
        :return:
        """
        filter_extensions = filter_extensions if filter_extensions else []

        files = folder.files
        self.context.load(files)
        self.context.execute_query()
        for cur_file in files:
            _url = cur_file.properties["ServerRelativeUrl"]
            if not filter_extensions or _url[:3] in filter_extensions:
                yield cur_file, cur_file.properties["ServerRelativeUrl"]

    def list_files_folders_recurs(self, folder):
        """
        Recursevly visit all the sub-folders and files inside a folder
        :param folder:
        :return:
        """
        for file, file_properties in self.list_files(folder):
            yield file
        for sub_folder, sub_folder_properties in self.list_folders(folder):
            for file in self.list_files_folders_recurs(sub_folder):
                yield file

    def download_file(self, relative_url):
        """
        Downloads as file by URL
        :param relative_url:
        :return:
        """
        response = File.open_binary(self.context, relative_url)
        return response.content
