import hashlib
import json
import logging
import requests

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)

from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)


def make_token(data):

    body = {"data": data}

    s = json.dumps(body, separators=(",", ":"))

    return hashlib.md5((s + "qhgas").encode()).hexdigest()


async def async_setup_entry(hass, entry, async_add_entities):

    card_id = entry.data["card_id"]

    async_add_entities([QHGasSensor(card_id)], True)


class QHGasSensor(SensorEntity):

    def __init__(self, card_id):

        self.card_id = card_id

        self._state = None

        self._volume = None

    @property
    def name(self):

        return "QH Gas Balance"

    @property
    def state(self):

        return self._state

    @property
    def extra_state_attributes(self):

        return {"volume": self._volume}

    def update(self):

        data = {"cardId": self.card_id, "userName": None, "nowPrice": None}

        token = make_token(data)

        body = {"data": data, "tokenS": token}

        try:

            r = requests.post(API_URL, json=body, timeout=10)

            res = r.json()

            self._state = res["data"]["balance"]

            self._volume = res["data"]["volume"]

        except Exception as e:

            _LOGGER.error(e)
