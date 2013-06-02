from pyramid.config import Configurator
import subprocess
import os
import signal
import atexit
from cloudy_tales.queue.client import create_queue_connection

CAKE_PROCESS = None


def main(global_config, **settings):
    '''
    This function returns a Pyramid WSGI application.
    '''
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=0)
    config.add_static_view('templates', 'templates')
    config.add_route('home', '/')
    config.include('sunny_tales.api.v0.template', route_prefix='/api/v0')
    config.scan()
    precompile()

    # Set up queue connection
    create_queue_connection()

    return config.make_wsgi_app()


def precompile():
    '''
    Precompile handlebar templates
    '''
    global CAKE_PROCESS
    # Add /usr/local/bin to path
    os.environ['PATH'] += os.pathsep + '/usr/local/bin'
    current_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(current_dir, 'static')
    run_npm_update = False
    try:
        return_val = 0
        os.chdir(static_dir)
        if run_npm_update:
            command = ['npm', 'update']
            return_val = subprocess.call(command)
        if return_val == 0:
            command = ['node_modules/coffee-script/bin/cake', '-w', 'true', 'compile']
            CAKE_PROCESS = subprocess.Popen(command)
    finally:
        os.chdir(current_dir)
    signal.signal(signal.SIGTERM, term_handler)


def term_handler():
    '''
    Place holder for signal termination handler
    '''
    pass


@atexit.register
def shut_down():
    '''
    Invoked when sunny shutsdown
    '''
    # Kill cake compile
    if CAKE_PROCESS:
        CAKE_PROCESS.kill()
