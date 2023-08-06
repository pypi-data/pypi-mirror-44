# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import contextlib
import docker
import alpy.utils
import alpy.node
import alpy.console


class ControllerBase:
    def __init__(self, *, link_count, timeout, test_name, test_description):
        alpy.utils.configure_logging()
        self._link_count = link_count
        self.timeout = timeout
        self._exit_stack = contextlib.ExitStack()
        self._skeleton = None
        self.docker_client = None
        self.qmp = None
        self.console = None
        logger = logging.getLogger(__name__)
        logger.info("Test name: " + test_name)
        logger.info("Test description: " + test_description)

    def __enter__(self):
        logger = logging.getLogger(__name__)
        with self._exit_stack:
            try:
                self._create()
            except:
                logger.error("Test failed")
                raise
            self._exit_stack = self._exit_stack.pop_all()
        logger.info("Enter test environment")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger = logging.getLogger(__name__)
        if exc_type:
            logger.error("Exit test environment with failure")
        else:
            logger.info("Exit test environment with success")
        test_passed = False
        try:
            self._exit_stack.close()

            if not exc_type:
                test_passed = True
        finally:
            if test_passed:
                logger.info("Test passed")
            else:
                logger.error("Test failed")

    def configure_interface(self, *, node, address, gateway=None):
        self._skeleton.configure_interface(node, address, gateway)

    def tap_interfaces(self):
        return [f"alpy{i}" for i in range(self._link_count)]

    def _create(self):

        self.docker_client = docker.from_env()
        self._exit_stack.callback(self.docker_client.close)

        self._skeleton = alpy.node.Skeleton(
            tap_interfaces=self.tap_interfaces(),
            docker_client=self.docker_client,
            timeout=self.timeout,
        )

        self._exit_stack.callback(self._skeleton.close)
        self._skeleton.create_tap_interfaces()
        qemu_args = self._get_qemu_args()

        self.qmp = self._exit_stack.enter_context(
            alpy.qemu.run(qemu_args, self.timeout)
        )

        self._skeleton.create()

        self.console = alpy.console.SerialConsole(timeout=self.timeout)

        self._exit_stack.callback(self.console.close)
        alpy.qemu.read_events(self.qmp)

    def _get_qemu_args(self):
        raise NotImplementedError
