# vim: set et sw=4:
import subprocess

from tornado import concurrent, gen, web
import tornado.ioloop

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
    @gen.coroutine
    def get(self):
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
        self.log.info(f'tree-download: {cmd}')
        self.handle_command_pipe(cmd)

        yield concurrent.Future()

    def handle_command_pipe(self, cmd):
        '''Pipe a command to a read event handler.'''
        # Via https://gist.github.com/saniaxxx/4a45ccc5e9a90101de64
        ioloop = tornado.ioloop.IOLoop.instance()
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True)
        pipe_fd = pipe.stdout.fileno()

        def pipe_to_write(*args):
            '''Write data from our pipe.
               Called with fd and an events constant.'''
            data = pipe.stdout.readline()
            if data:
                self.write(data)
                self.flush()
            elif pipe.poll() is not None:
                ioloop.remove_handler(pipe_fd)
                self.finish()

        # call pipe_to_write when pipe_fd gets a read I/O event
        ioloop.add_handler(pipe_fd, pipe_to_write, ioloop.READ)

class TreeDownload(Configurable):
    compression = Unicode(u"gzip", help="Compression type.", config=True)
