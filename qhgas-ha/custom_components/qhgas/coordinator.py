from datetime import timedelta
import logging
import hashlib
import aiohttp

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

DOMAIN = "qhgas"
SCAN_INTERVAL = 3600

_LOGGER = logging.getLogger(__name__)

_LOGGER.error("QHGas coordinator 已加载")

class QHGasCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, card_id):

        self.hass = hass

        self.card_id = card_id

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):

        balance = await self.get_balance()

        return {"balance": balance}

    async def get_balance(self):

        try:

            # 生成 tokenS

            token = hashlib.md5((self.card_id + "qhgas").encode("utf-8")).hexdigest()

            url = "http://wkf.qhgas.com/rs/WX/getLastBalance"

            payload = {"data": {"cardId": self.card_id, "userName": None, "nowPrice": None}, "tokenS": token}

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "Referer": "http://wkf.qhgas.com/",
            }

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    url, json=payload, headers=headers, timeout=15
                ) as response:

                    _LOGGER.warning("QHGas API 响应状态码: %s", response.status)

                    if response.status != 200:
                        _LOGGER.error("获取燃气余额失败: API 返回错误状态码 %s", response.status)
                        return None

                    try:
                        data = await response.json()
                        _LOGGER.warning("QHGas API 返回: %s", data)

                        # 根据实际返回结构修改
                        if data.get("resultValue") == 0:
                            balance = data.get("balance")
                            now_price = data.get("nowPrice")
                            battery_level = data.get("battery_level")
                            return {
                                "balance": float(balance) if balance else 0.0,
                                "nowPrice": float(now_price) if now_price else 0.0,
                                "battery_level": float(battery_level) if battery_level else 0.0,
                                "valveState": data.get("valveState", "未知"),
                                "signal": data.get("signal", "未知")
                            }

                        return None
                    except Exception as json_error:
                        _LOGGER.error("解析 API 返回数据失败: %s", json_error)
                        return None

        except Exception as e:

            _LOGGER.error("获取燃气余额失败: %s", e)

            return None
