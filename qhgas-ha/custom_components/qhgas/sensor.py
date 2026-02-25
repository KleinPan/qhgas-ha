from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "qhgas"

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # 创建多个传感器实体，分别对应不同的数据字段
    async_add_entities([
        QHGasBalanceSensor(coordinator, entry),
        QHGasPriceSensor(coordinator, entry),
        QHGasBatterySensor(coordinator, entry),
        QHGasValveSensor(coordinator, entry),
        QHGasSignalSensor(coordinator, entry)
    ], True)

class QHGasBalanceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.card_id = coordinator.card_id
        self._attr_name = f"QH Gas {self.card_id} Balance"
        self._attr_unique_id = f"qhgas_{self.card_id}_balance"
        self._attr_native_unit_of_measurement = "元"

    @property
    def native_value(self):
        return self.coordinator.data.get("balance", 0.0)

class QHGasPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.card_id = coordinator.card_id
        self._attr_name = f"QH Gas {self.card_id} Price"
        self._attr_unique_id = f"qhgas_{self.card_id}_price"
        self._attr_native_unit_of_measurement = "元/m³"

    @property
    def native_value(self):
        return self.coordinator.data.get("nowPrice", 0.0)

class QHGasBatterySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.card_id = coordinator.card_id
        self._attr_name = f"QH Gas {self.card_id} Battery"
        self._attr_unique_id = f"qhgas_{self.card_id}_battery"
        self._attr_native_unit_of_measurement = "V"

    @property
    def native_value(self):
        return self.coordinator.data.get("battery_level", 0.0)

class QHGasValveSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.card_id = coordinator.card_id
        self._attr_name = f"QH Gas {self.card_id} Valve"
        self._attr_unique_id = f"qhgas_{self.card_id}_valve"

    @property
    def native_value(self):
        return self.coordinator.data.get("valveState", "未知")

class QHGasSignalSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.card_id = coordinator.card_id
        self._attr_name = f"QH Gas {self.card_id} Signal"
        self._attr_unique_id = f"qhgas_{self.card_id}_signal"

    @property
    def native_value(self):
        return self.coordinator.data.get("signal", "未知")