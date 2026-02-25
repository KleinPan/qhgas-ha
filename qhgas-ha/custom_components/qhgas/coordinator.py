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
        data = await self.get_balance()

        if data is not None:
            return data
        
        return {
            "balance": 0.0,
            "nowPrice": 0.0,
            "battery_level": 0.0,
            "valveState": "未知",
            "signal": "未知"
        }

    async def get_balance(self):
        try:
            # 按照用户提供的脚本生成 token
            s = '{"data":{"cardId":"' + self.card_id + '","userName":null,"nowPrice":null}}'
            token = hashlib.md5((s + "qhgas").encode()).hexdigest()

            url = "http://wkf.qhgas.com/rs/WX/getLastBalance"

            # 按照用户提供的格式构建请求数据
            data = s[:-1] + ',"tokenS":"' + token + '"}'

            # 使用用户提供的请求头
            headers = {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "MicroMessenger",
                "Referer": "http://wkf.qhgas.com/index.html"
            }

            _LOGGER.warning("QHGas API 请求数据: %s", data)
            _LOGGER.warning("QHGas API 请求头: %s", headers)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=data, headers=headers, timeout=15
                ) as response:
                    _LOGGER.warning("QHGas API 响应状态码: %s", response.status)

                    # 即使 API 返回错误，也尝试获取更多信息
                    try:
                        response_text = await response.text()
                        _LOGGER.warning("QHGas API 响应内容: %s", response_text)
                    except:
                        pass

                    if response.status != 200:
                        _LOGGER.error("获取燃气余额失败: API 返回错误状态码 %s", response.status)
                        return None

                    try:
                        data = await response.json()
                        _LOGGER.warning("QHGas API 返回: %s", data)

                        # 按照用户提供的返回格式解析
                        if data.get("resultValue") == 0:
                            return {
                                "balance": float(data.get("balance", 0)),
                                "nowPrice": float(data.get("nowPrice", 0)),
                                "battery_level": float(data.get("battery_level", 0)),
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