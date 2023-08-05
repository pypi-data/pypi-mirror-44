"""Subscription manager for Graph QL websocket."""

import asyncio
import json
import logging
from time import time

import websockets

_LOGGER = logging.getLogger(__name__)

STATE_STARTING = "starting"
STATE_RUNNING = "running"
STATE_STOPPED = "stopped"


class SubscriptionManager:
    """Subscription manager."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, loop, init_payload, url):
        """Create resources for websocket communication."""
        self.loop = loop
        self.subscriptions = {}
        self._url = url
        self._state = None
        self.websocket = None
        self._retry_timer = None
        self._client_task = None
        self._wait_time_before_retry = 15
        self._session_id = 0
        self._init_payload = init_payload
        self._show_connection_error = True
        self._is_running = False

    def start(self):
        """Start websocket."""
        _LOGGER.debug("Start state %s.", self._state)
        if self._state == STATE_RUNNING:
            return
        self._state = STATE_STARTING
        self._cancel_client_task()
        self._client_task = self.loop.create_task(self.running())
        for subscription in self.subscriptions.copy():
            callback, sub_query = self.subscriptions.pop(subscription, (None, None))
            _LOGGER.debug("Removed, %s", subscription)
            if callback is None:
                continue
            _LOGGER.debug("Add subscription %s", callback)
            self.loop.create_task(self.subscribe(sub_query, callback))

    @property
    def is_running(self):
        """Return if client is running or not."""
        return self._is_running

    async def running(self):
        """Start websocket connection."""
        # pylint: disable=too-many-branches, too-many-statements
        await self._close_websocket()
        try:
            _LOGGER.debug("Starting")
            self.websocket = await websockets.connect(
                self._url, subprotocols=["graphql-subscriptions"]
            )
            self._state = STATE_RUNNING
            _LOGGER.debug("Running")
            await self.websocket.send(
                json.dumps({"type": "init", "payload": self._init_payload})
            )

            k = 0
            while self._state == STATE_RUNNING:
                try:
                    msg = await asyncio.wait_for(self.websocket.recv(), timeout=30)
                except asyncio.TimeoutError:
                    k += 1
                    if k > 10:
                        if self._show_connection_error:
                            _LOGGER.error("No data, reconnecting.")
                            self._show_connection_error = False
                        self._is_running = False
                        return
                    _LOGGER.debug(
                        "No websocket data in 30 seconds, checking the connection."
                    )
                    try:
                        pong_waiter = await self.websocket.ping()
                        await asyncio.wait_for(pong_waiter, timeout=10)
                    except asyncio.TimeoutError:
                        if self._show_connection_error:
                            _LOGGER.error(
                                "No response to ping in 10 seconds, " "reconnecting."
                            )
                            self._show_connection_error = False
                        self._is_running = False
                        return
                    continue
                k = 0
                self._is_running = True
                await self._process_msg(msg)
                self._show_connection_error = True
        except websockets.exceptions.InvalidStatusCode:
            if self._show_connection_error:
                _LOGGER.error("Connection error", exc_info=True)
                self._show_connection_error = False
            else:
                _LOGGER.debug("Connection error", exc_info=True)
        except websockets.exceptions.ConnectionClosed:
            if self._show_connection_error and self._state != STATE_STOPPED:
                _LOGGER.error("Connection error", exc_info=True)
                self._show_connection_error = False
            else:
                _LOGGER.debug("Connection error", exc_info=True)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error("Unexpected error", exc_info=True)
        finally:
            await self._close_websocket()
            if self._state != STATE_STOPPED:
                _LOGGER.debug("Reconnecting")
                self._state = STATE_STOPPED
                self.retry()
            _LOGGER.debug("Closing running task.")

    async def stop(self, timeout=10):
        """Close websocket connection."""
        _LOGGER.debug("Stopping client.")
        start_time = time()
        self._cancel_retry_timer()

        for subscription_id in range(len(self.subscriptions)):
            _LOGGER.debug("Sending unsubscribe: %s", subscription_id)
            await self.unsubscribe(subscription_id)

        while (
            timeout > 0
            and self.websocket is not None
            and not self.subscriptions
            and (time() - start_time) < timeout / 2
        ):
            await asyncio.sleep(0.1, loop=self.loop)

        self._state = STATE_STOPPED
        while (
            timeout > 0
            and self.websocket is not None
            and not self.websocket.closed
            and (time() - start_time) < timeout
        ):
            await asyncio.sleep(0.1, loop=self.loop)

        await self._close_websocket()
        self._cancel_client_task()
        _LOGGER.debug("Server connection is stopped")

    def retry(self):
        """Retry to connect to websocket."""
        _LOGGER.debug("Retry, state: %s", self._state)
        if self._state in [STATE_STARTING, STATE_RUNNING]:
            _LOGGER.debug("Skip retry since state: %s", self._state)
            return
        self._cancel_retry_timer()
        self._state = STATE_STARTING
        self._retry_timer = self.loop.call_later(
            self._wait_time_before_retry, self.start
        )
        _LOGGER.debug(
            "Reconnecting to server in %i seconds.", self._wait_time_before_retry
        )

    async def subscribe(self, sub_query, callback):
        """Add a new subscription."""
        while True:
            if (
                self.websocket is None
                or not self.websocket.open
                or not self._state == STATE_RUNNING
            ):
                await asyncio.sleep(1, loop=self.loop)
                continue

            current_session_id = self._session_id
            self._session_id += 1
            subscription = {
                "query": sub_query,
                "type": "subscription_start",
                "id": current_session_id,
            }
            json_subscription = json.dumps(subscription)
            await self.websocket.send(json_subscription)
            self.subscriptions[current_session_id] = (callback, sub_query)
            _LOGGER.debug("New subscription %s", current_session_id)
            return current_session_id

    async def unsubscribe(self, subscription_id):
        """Unsubscribe."""
        if self.websocket is None or not self.websocket.open:
            _LOGGER.warning("Websocket is closed.")
            return
        await self.websocket.send(
            json.dumps({"id": subscription_id, "type": "subscription_end"})
        )
        if self.subscriptions and subscription_id in self.subscriptions:
            self.subscriptions.pop(subscription_id)

    async def _close_websocket(self):
        if self.websocket is None:
            return
        try:
            await self.websocket.close()
        finally:
            self.websocket = None

    async def _process_msg(self, msg):
        """Process received msg."""
        result = json.loads(msg)
        _LOGGER.debug("Recv, %s", result)

        subscription_id = result.get("id")
        if subscription_id is None:
            return

        callback, _ = self.subscriptions.get(subscription_id, (None, None))
        if callback is None:
            _LOGGER.debug("Unknown id %s.", subscription_id)
            return

        if result.get("type", "") == "complete":
            _LOGGER.debug("Unsubscribe %s successfully.", subscription_id)
            return

        data = result.get("payload")
        if data is None:
            return

        await callback(data)

    def _cancel_retry_timer(self):
        if not self._retry_timer:
            return
        try:
            self._retry_timer.cancel()
        finally:
            self._retry_timer = None

    def _cancel_client_task(self):
        if not self._client_task:
            return
        try:
            self._client_task.cancel()
        finally:
            self._client_task = None
