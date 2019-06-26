import asyncio

from tornado import web

from traitlets import Unicode
from traitlets.config.configurable import Configurable

from notebook.base.handlers import IPythonHandler

def attachment_suffix(compression):
    '''Determines the conventional suffix of the compressed download.'''
    if compression == 'zip':     return compression
    elif compression == 'gzip':  return 'tar.gz'
    elif compression == 'bzip2': return 'tar.bz2'
    else:                        return f'tar.{compression}'

def command(compression, path):
    '''Returns a command that can compress our path to standard out.'''
    if compression == 'zip':
        return ['zip', '-q', '-r', '-', path]
    else:
        return ['tar', '-c', f'--{compression}', '-f', '-', path]

def friendly_name(name, path, suffix):
    '''Return a friendly name for the downloaded file.'''
    # If we're at the top-level, just return what the frontend provides (the
    # hostname). Otherwise return the same followed by some path context.
    normalized_path = path.replace('/', '_')
    if path == '.':
        return f'{name}.{suffix}'
    else:
        return f'{name}-{normalized_path}.{suffix}'

class TreeDownloadHandler(IPythonHandler):

    def initialize(self):
        super().initialize()
        self.c = TreeDownload(config=self.config)

    @web.authenticated
    async def get(self):
        '''Accepts arguments:
             name: a hint for the downloaded filename,
             path: path to the directory to download,
             compression: compression type, e.g. zip, gzip, bzip2, etc.
        '''
        name = self.get_argument('name')
        if name == '': name = 'tree'

        path = self.get_argument('path', '.')
        if path == '': path = '.'

        compression = self.get_argument('compression', self.c.compression)
        suffix = attachment_suffix(compression)

        filename = friendly_name(name, path, suffix)

        self.set_header('content-type', 'application/octet-stream')
        self.set_header('cache-control', 'no-cache')
        self.set_header('content-disposition',
            f'attachment; filename="{filename}"'
        )

        cmd = command(compression, path)
        p = await asyncio.create_subprocess_exec(*cmd,
            stdout=asyncio.subprocess.PIPE)
        async for line in p.stdout:
            self.write(line)
        await p.wait()
        self.finish()

class TreeDownload(Configurable):
    compression = Unicode(u"gzip", help="Compression type.", config=True)
