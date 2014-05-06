#!/usr/bin/env python

"""A Python command-line wrapper with github3.py library to access GitHub Gist.
"""

import os
import sys
import uuid
from functools import wraps
from getpass import getpass, getuser

import click
import requests
from github3 import authorize, login
from github3.models import GitHubError

try:
    from urlparse import urlparse
except ImportError:
    # py3k
    from urllib.parse import urlparse

def auth_check(func):
    """Decorator to note which object methods require authorization"""
    @wraps(func)
    def check_wrapper(self, *args, **kwargs):
        """A wrapper to check if a token exists"""
        if not kwargs.get('anonymous'):
            try:
                with open(os.path.expanduser('~/.pgist'), 'r') as tkf:
                    self.token = tkf.readline()
                self.github = login(token=self.token)
            except IOError:
                raise SystemExit('Please use `pgist --login` authenticate ' \
                        'gist on this computer')
        try:
            return func(self, *args, **kwargs)
        except GitHubError as ghe:
            if ghe.code in (401, 403):
                raise SystemExit('Your current gist authorize is bad, ' \
                        'please use `pgist --login` to authenticate it again!')
            raise SystemExit(ghe + '\nPlease report this bug to the author!')
    return check_wrapper

def token_request():
    """Request app token from GitHub to operate gists"""
    try:
        prompt = raw_input
    except NameError:
        prompt = input
    user = prompt('GitHub username(default is {0}): '.format(getuser())) \
            or getuser()
    password = ''

    while not password:
        password = getpass('GitHub password for {0}: '.format(user))

    # Ensure github tokens have a unique description
    note = 'the unique pgist -> {0}'.format(uuid.uuid4())
    note_url = 'https://github.com/douglarek/pgist'
    scopes = ['gist']

    try:
        auth = authorize(user, password, scopes, note, note_url)
    except GitHubError as ghe:
        if 'two-factor' in str(ghe):
            raise SystemExit('GitHub 2-factor auth is not supported ' \
                    'temporarily o(>_<)o, please disable it to use pgist !')
        raise SystemExit('Gist authorize failed, please check your username '\
                'or password!')

    with open(os.path.expanduser('~/.pgist'), 'w') as tkf:
        tkf.write(auth.token)

    click.echo('Done ...')

def url_shorten(long_url):
    """Shorten a long url with git.io service"""
    req = requests.post('http://git.io', data={'url' : long_url})
    return req.headers['location']

def upload_files(files):
    """Build up uploaded or updated files' structure"""
    _upload_files = {}
    for obj in files:
        content = obj.readlines()
        if not content:
            continue
        _upload_files[obj.name.split('/')[-1]] = {'content' : \
                ''.join(content)}
        obj.close()
        del obj

    if not _upload_files:
        raise SystemExit('All of your files are empty, WTF?')

    return _upload_files

def find_gist_by_id(github, _id):
    """Find a gist by _id"""
    dest = None
    for gist in github.iter_gists():
        if _id == gist.id or _id == gist.html_url:
            dest = gist
            break

    if dest is None:
        raise SystemExit('The gist ID or URL is not found, is it right?')

    return dest

def get_id(_id):
    """Convert _id(ID or URL) to ID"""
    result = urlparse(_id)
    if result.path:
        return result.path.split('/')[-1]
    raise SystemExit('Your url(id): {0} is invalid !'.format(_id))

class Gist(object):
    """Define known gist operations"""

    def __init__(self):
        self.token, self.github = None, None

    @auth_check
    def list_gists(self, _all=False):
        """List all gists or public only ones"""
        click.echo('List of {0} gists: \n'.format(['public','all'][_all]))
        if _all:
            for gist in self.github.iter_gists():
                click.echo('{0}{1}'.format(\
                        [g.name for g in gist.iter_files()][0].ljust(30), \
                        gist.html_url))
        else:
            for gist in self.github.iter_gists():
                if gist.is_public():
                    click.echo('{0}{1}'.format(\
                            [g.name for g in gist.iter_files()][0].ljust(30), \
                            gist.html_url))

    @auth_check
    def create_gist(self,
                    description=None,
                    files=(),
                    public=True,
                    anonymous=False,
                    short_url=False):
        """Create public, private or anonymous gists"""
        if description is None:
            description = ''

        if anonymous:
            from github3 import create_gist
            gist = create_gist(description, upload_files(files))
        else:
            gist = self.github.create_gist(description, upload_files(files), \
                    public)

        click.echo(url_shorten(gist.html_url) if short_url else gist.html_url)

    @auth_check
    def update_gist(self,
                    _id,
                    description=None,
                    files=()):
        """Update a gist"""
        if description is None:
            description = ''

        dest = find_gist_by_id(self.github, get_id( _id))

        if dest.edit(description, upload_files(files)):
            click.echo('<{0}> has been updated successfully.'.format(dest.html_url))

    @auth_check
    def delete_gist(self, _id):
        """Delete a gist by _id"""
        dest = find_gist_by_id(self.github, get_id(_id))
        if dest.delete():
            click.echo('<{0}> has been deleted successfully.'.format(dest.html_url))

    @auth_check
    def fork_gist(self, _id):
        """Fork a gist by ID or URL"""
        try:
            new = self.github.gist(get_id(_id)).fork()
        except AttributeError:
            raise SystemExit('The gist {0} is not found !'.format(_id))
        if new is None:
            raise SystemExit('Enha, maybe you are forking yourself ?')
        click.echo('{0} is forked to {1}'.format(_id, new.html_url))


def print_help(ctx, value):
    """A callback func, when type `-h`, show help"""
    if not value:
        return
    click.echo(ctx.get_help())
    ctx.exit()

@click.command()
@click.option('-l', 'list_', is_flag=True, help='List public gists, with `-A` list all ones')
@click.option('-A', 'all_', is_flag=True)
@click.option('-s', 'shorten', is_flag=True, help='Shorten the gist URL using git.io')
@click.option('-u', 'update', metavar='URL/ID', help='Update an existing gist')
@click.option('-d', 'desc', metavar='DESCRIPTION', help='Adds a description to your gist')
@click.option('-D', 'delete', metavar='URL/ID', help='Detele an existing gist')
@click.option('-f', 'fork', metavar='URL/ID', help='Fork an existing gist')
@click.option('-p', 'private', is_flag=True, help='Makes your gist private')
@click.option('-a', 'anonymous', is_flag=True, help='Create an anonymous gist')
@click.option('--login', 'login', is_flag=True, help='Create an anonymous gist')
@click.option('-h', is_flag=True, callback=print_help, expose_value=False, is_eager=True)
@click.argument('files', nargs=-1, type=click.File())
@click.pass_context
def cli(ctx, files, list_, all_, shorten, update, desc, delete, fork, private, anonymous, login):
    """A Python command-line wrapper with github3.py library to access GitHub gists"""
    gist = Gist()

    if list_:
        gist.list_gists(_all=all_)
    elif update and files:
        gist.update_gist(update, desc, files)
    elif delete:
        gist.delete_gist(delete)
    elif files:
        gist.create_gist(desc, files, [True, False][private], anonymous=anonymous, short_url=shorten)
    elif login:
        token_request()
    else:
        click.echo(ctx.get_help())

if __name__ == '__main__':
    cli()
