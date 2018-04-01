import click
import re

from unshortenit import UnshortenIt


class UrlParamType(click.ParamType):
    name = 'url'
    _regex = re.compile(r'^https?\://.*')

    def convert(self, value, param, ctx):
        if not self._regex.match(value):
            self.fail('%s is not a valid url' % value, param, ctx)
        return value


URL = UrlParamType()


@click.command()
@click.option('--module', type=str, help='Module to use for unshortening the url.')
@click.option('--follow-nested', is_flag=True, help='Follow nested unshorteners.', default=False)
@click.argument('url', type=URL)
def cli(module, url, follow_nested):
    unshortener = UnshortenIt()
    print(unshortener.unshorten(url, module, unshorten_nested=follow_nested))
