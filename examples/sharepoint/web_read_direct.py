from spoklient.runtime.auth.authentication_context import AuthenticationContext
from spoklient.runtime.client_request import ClientRequest
from spoklient.runtime.utilities.request_options import RequestOptions
from settings import settings
import json

from spoklient.sharepoint.client_context import ClientContext

if __name__ == '__main__':
    context_auth = AuthenticationContext(url=settings['url'])
    if context_auth.acquire_token_for_user(username=settings['user_credentials']['username'],
                                           password=settings['user_credentials']['password']):
        """Read Web client object"""
        ctx = ClientContext(settings['url'], context_auth)

        request = ClientRequest(ctx)
        options = RequestOptions("{0}/_api/web/".format(settings['url']))
        options.set_header('Accept', 'application/json')
        options.set_header('Content-Type', 'application/json')
        data = ctx.execute_request_direct(options)
        s = json.loads(data.content)
        web_title = s['Title']
        print("Web title: {0}".format(web_title))

    else:
        print(context_auth.get_last_error())
