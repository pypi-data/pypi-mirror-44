# Copyright 2015 Jared Rodriguez (jared.rodriguez@rackspace.com)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import time

from mercury_agent.capabilities import capability
from mercury_agent.configuration import get_configuration
from mercury.common.clients.rpc.backend import BackEndClient
from mercury.common.exceptions import fancy_traceback_short, parse_exception

from press.configuration.util import configuration_from_file
from press.exceptions import PressCriticalException
from press.log import setup_logging
from press.plugin_init import init_plugins
from press.press import PressOrchestrator
from press.press_cli import parse_args
from press.hooks.hooks import clear_hooks


log = logging.getLogger(__name__)


def cleanup_thread():
    # Clear logging handlers!
    del logging.getLogger('press').handlers[:]
    # Clear hooks
    clear_hooks()


# noinspection PyBroadException
def entry(run_configuration, mercury_press_configuration):
    """

    :param run_configuration: The press state file
    :param mercury_press_configuration: press environment configuration from
    mercury-agent.yaml
    :return:
    """
    log.info('Initializing plugins')
    init_plugins(run_configuration,
                 mercury_press_configuration.get('plugins', {}).get(
                     'scan_directories'),
                 mercury_press_configuration.get('plugins', {}).get(
                     'enabled'
                 ))

    return_data = {}

    p = None
    try:
        p = PressOrchestrator(
            run_configuration,
            mercury_press_configuration.get('paths', {}).get(
                'parted', 'parted'),
            mercury_press_configuration.get('deployment_root', '/mnt/press'),
            mercury_press_configuration.get('staging_directory', '/.press'),
            mercury_press_configuration.get('layout', {}).get(
                'use_fibre_channel', False
            ),
            mercury_press_configuration.get('layout', {}).get(
                'loop_only', False
            ),
            mercury_press_configuration.get('partition_table', {}).get(
                'partition_start', 1048576
            ),
            mercury_press_configuration.get('partition_table', {}).get(
                'alignment', 1048576
            ),
            mercury_press_configuration.get('volume_group', {}).get(
                'pe_size', '4MiB'
            )
        )
    except Exception:
        exec_dict = parse_exception()
        log.error('Error during initialization: {}'.format(
            fancy_traceback_short(exec_dict)))
        return_data = {'error': True, 'message': 'Error during initialization',
                       'exception': exec_dict}
        cleanup_thread()

    if p:
        try:
            p.run()
        except Exception:
            exec_dict = parse_exception()
            log.error('Error during deployment: {}'.format(
                fancy_traceback_short(exec_dict)))
            return_data = {'error': True,
                           'message': 'Error during initialization',
                           'exception': exec_dict}
        finally:
            if p.layout.committed:
                time.sleep(2)
                p.teardown()

            cleanup_thread()

    return return_data


def add_mercury_plugin_data(press_configuration, task_id):
    temp_plugins = press_configuration.get('plugins', [])
    if 'mercury' not in temp_plugins:
        temp_plugins.append('mercury')
        press_configuration['plugins'] = temp_plugins

    press_configuration['mercury'] = {
        'task_id': task_id,
        'backend_zurl': get_configuration().agent.remote.backend_url
    }


@capability('press', description='Native press support in mercury', serial=True,
            kwarg_names=['configuration'], task_id_kwargs=True)
def press_native(**kwargs):
    press_configuration = kwargs['configuration']
    task_id = kwargs['task_id']

    mercury_configuration = get_configuration()
    add_mercury_plugin_data(press_configuration, task_id)

    backend_client = BackEndClient(
        mercury_configuration.agent.remote.backend_url)
    log.info('Starting press')
    start = time.time()
    backend_client.update_task({'task_id': task_id,
                                'action': 'Press: Launching'})
    return_data = entry(press_configuration,
                        mercury_configuration.get('press', {}))
    return_data['press_execution_time'] = time.time() - start
    return return_data
