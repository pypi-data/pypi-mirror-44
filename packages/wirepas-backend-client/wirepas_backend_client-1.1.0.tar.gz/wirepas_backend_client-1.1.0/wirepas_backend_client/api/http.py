# Copyright 2018 Wirepas Ltd. All Rights Reserved.
#
# See file LICENSE.txt for full license details.
#

import multiprocessing
import http.server
import time
import urllib
import binascii
import socketserver

from threading import Thread

from .stream import StreamObserver
from ..tools import Settings
from ..tools import ExitSignal
from .. import messages
from functools import wraps
from ..messages.interface import MessageManager
from .mqtt import Topics
import queue

# Following globals are used for delivering data between
# HTTPObserver class and HTTPServer class
http_tw_queue = None
gateways_and_sinks = {}  # { 'gw_id': {'sink_id': {'started': True/False, 'app_config_seq': int, 'app_config_diag': int, 'app_config_data': bytes }}}
mqtt_topics = Topics()

class SinkAndGatewayStatusObserver(Thread):
    def __init__(self, exit_signal, gw_status_queue, logger):
        super(SinkAndGatewayStatusObserver, self).__init__()
        self.exit_signal = exit_signal
        self.gw_status_queue = gw_status_queue
        self.logger = logger

    def run(self):
        while not self.exit_signal.is_set():
            try:
                status_msg = self.gw_status_queue.get(block=True, timeout=20)
                self.logger.debug('HTTP status_msg={}'.format(status_msg))
                if 'sink_id' in status_msg:
                    sink = { status_msg['sink_id']: { 'started': status_msg['started'],
                                                      'app_config_seq': status_msg['app_config_seq'],
                                                      'app_config_diag': status_msg['app_config_diag'],
                                                      'app_config_data': status_msg['app_config_data']}}
                    if status_msg['gw_id'] in gateways_and_sinks:
                        gateways_and_sinks[status_msg['gw_id']].update(sink)
                    else:
                        gateways_and_sinks[status_msg['gw_id']] = sink
                else:
                    # No sink defined
                    if status_msg['started']:
                        self.logger.error('ERROR: sink_id must be specified when setting started=True')
                    else:
                        # Whole gateway is gone, mark all sinks of it as not started
                        for sink in gateways_and_sinks[status_msg['gw_id']]:
                            if 'started' in sink:
                                sink['started'] = False
            except queue.Empty:
                self.logger.debug('HTTP Server gateways_and_sinks={}'.format(gateways_and_sinks))
                # mqtt client does not get notified if GW configuration changes,
                # thus we have to poll GW to have its configuration. Fortunately
                # the receiver part already exists, it is just matter of sending
                # the request time to time. There is pending request to get
                # GW event also in case the amount of sinks in GW changes, when
                # implemented, this "polling time to time"-part can be removed.
                global http_tx_queue
                global mqtt_topics
                for gateway_id, sinks in gateways_and_sinks.items():
                    request = mqtt_topics.request_message(
                                 "get_configs", dict(gw_id=gateway_id))
                    # Insert the message(s) tx queue
                    http_tx_queue.put(request)


class HTTPSettings(Settings):
    """HTTP Settings"""

    def __init__(self, settings: Settings)-> 'HttpSettings':

        super(HTTPSettings, self).__init__(settings)

        self.hostname = self.http_host
        self.port = self.http_port


class HTTPObserver(StreamObserver):
    """
    HTTPObserver has three Observer functions:
    monitors the web traffic and sends requests to mqtt broker,
    monitors mqtt messages about sending status (not implemented ### TODO ###),
    monitors what gateways and sinks are online.
    """

    def __init__(self,
                 http_settings: Settings,
                 start_signal: multiprocessing.Event,
                 exit_signal: multiprocessing.Event,
                 tx_queue: multiprocessing.Queue,
                 rx_queue: multiprocessing.Queue,
                 gw_status_queue: multiprocessing.Queue,
                 logger=None) -> 'HTTPObserver':
        super(HTTPObserver, self).__init__(start_signal=start_signal,
                                           exit_signal=exit_signal,
                                           tx_queue=tx_queue,
                                           rx_queue=rx_queue)

        self.logger = logger or logging.getLogger(__name__)

        self.port = http_settings.port
        self.hostname = http_settings.hostname
        self.gw_status_queue = gw_status_queue
        global http_tx_queue
        http_tx_queue = tx_queue

        Handler = HTTPServer
        while not self.exit_signal.is_set():
            try:
                # Crate the HTTP server.
                self.httpd = socketserver.TCPServer((self.hostname, self.port), Handler)
                self.logger.debug('HTTP Server is serving at port: {}'.format(self.port))
                break
            except Exception as ex:
                self.logger.error('ERROR: Opening HTTP Server port {} failed. Reason: "{}". Retrying after 10 seconds.'.format(self.port, ex))
                time.sleep(10)

        self.status_observer = SinkAndGatewayStatusObserver(self.exit_signal,
                                                            self.gw_status_queue,
                                                            self.logger)


    def run(self):
        # Start status observer thread
        self.status_observer.start()

        # Run until killed.
        while not self.exit_signal.is_set():
            # Handle a http request.
            self.httpd.handle_request()

        self.logger.debug('HTTP Control server killed')
        self.status_observer.join()

    def kill(self):
        '''Kill the gateway thread.
        '''

        # Send a dummy request to let the handle_request to proceed.
        urllib.urlopen("http://{}:{}".format(self.hostname,self.port)).read()


class HTTPServer(http.server.SimpleHTTPRequestHandler):
    '''A simple HTTP server class.

    Only overrides the do_GET from the HTTP server so it catches
    all the GET requests and processes them into commands.
    '''

    def do_GET(self):
        '''Process a single HTTP GET request.
        '''

        print("GET request: {}".format(self.path))

        # Parse into commands and parameters
        splitted = urllib.parse.urlsplit(self.path)
        command = splitted.path.split('/')[1]

        # Convert the parameter list into a dictionary.
        params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))

        # By default assume good from people and their code
        http_response = 200

        # Go through all gateways and sinks that are currently known to be online.
        for gateway_id, sinks in gateways_and_sinks.items():
            for sink_id, sink in sinks.items():

                if command == "datatx":

                    if not sink['started']:
                        # Do not attempt to send to sink that doesn't have stack started
                        continue
                    try:
                        dest_add=int(params['destination'])
                        src_ep=int(params['source_ep'])
                        dst_ep=int(params['dest_ep'])
                        qos=int(params['qos'])
                        payload=binascii.unhexlify(params['payload'])
                        try:
                            is_unack_csma_ca = params['fast'] in ['true', '1', 'yes', 'y']
                        except KeyError:
                            is_unack_csma_ca = False
                        try:
                            hop_limit = int(params['hoplimit'])
                        except KeyError:
                            hop_limit = 0
                        try:
                            count = int(params['count'])
                        except KeyError:
                            count = 1

                        while (count):
                            count -= 1

                            # Create sendable message.
                            global http_tx_queue
                            message = mqtt_topics.request_message(
                                          "send_data",
                                          dict(sink_id=sink_id,
                                               gw_id=gateway_id,
                                               dest_add=dest_add,
                                               src_ep=src_ep,
                                               dst_ep=dst_ep,
                                               qos=qos,
                                               payload=payload,
                                               is_unack_csma_ca=is_unack_csma_ca,
                                               hop_limit=hop_limit))
                            # Insert the message(s) tx queue
                            http_tx_queue.put(message)

                    except:
                        http_response = 500

                elif command == "start":

                    new_config = {'started': True}
                    message = mqtt_topics.request_message(
                                  "set_config",
                                  dict(sink_id=sink_id,
                                       gw_id=gateway_id,
                                       new_config=new_config))
                    http_tx_queue.put(message)

                elif command == "stop":

                    new_config = {'started': False}
                    message = mqtt_topics.request_message(
                                 "set_config",
                                 dict(sink_id=sink_id,
                                      gw_id=gateway_id,
                                      new_config=new_config))
                    http_tx_queue.put(message)

                elif command == "setconfig":

                    try:
                        seq=int(params['seq'])
                    except KeyError:
                        if sink['app_config_seq'] == 254:
                            seq = 1
                        else:
                            seq = sink['app_config_seq'] + 1
                    try:
                        diag=int(params['diag'])
                    except KeyError:
                        diag = sink['app_config_diag']
                    try:
                        data=bytes.fromhex(params['data'])
                    except KeyError:
                        data = sink['app_config_data']
                    new_config={'app_config_diag': diag,
                                'app_config_data': data,
                                'app_config_seq': seq
                               }
                    message = mqtt_topics.request_message("set_config",
                                                          dict(sink_id=sink_id,
                                                               gw_id=gateway_id,
                                                               new_config=new_config,
                                                              )
                                                         )
                    http_tx_queue.put(message)
                else:
                    http_response = 500
        # Respond to front-end
        self.send_response(http_response)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Wirepas Python Gateway", 'utf-8'))
        self.wfile.write(bytes(" ... Command: {}".format(command), 'utf-8'))
        self.wfile.write(bytes(" ... Parameters: {}".format(params), 'utf-8'))
