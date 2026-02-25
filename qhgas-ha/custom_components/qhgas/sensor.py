from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "qhgas"


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(

        [QHGasSensor(coordinator, entry)],

        True

    )


class QHGasSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, entry):

        super().__init__(coordinator)

        self.card_id = coordinator.card_id

        self._attr_name = f"QH Gas {self.card_id}"

        self._attr_unique_id = f"qhgas_{self.card_id}"

        self._attr_native_unit_of_measurement = "元"


    @property
    def native_value(self):

        return self.coordinator.data["balance"]