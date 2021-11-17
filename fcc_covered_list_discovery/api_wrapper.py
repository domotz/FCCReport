import logging
from datetime import datetime
import requests

_logger = logging.getLogger(__file__)


class ApiWrapper:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self._device_types = None
        self.count = 0

    def _network_http_request(self, resource):
        headers = {"Accept": "application/json", "X-Api-Key": self.api_key}
        url = f"{self.endpoint}/{resource}"
        res = requests.get(url, params={}, headers=headers)
        self.count += 1
        if res.status_code > 400:
            _logger.error("Erroneous request: %s", url)
            raise RuntimeError(res.json())

        return res.json()

    def api_call_counter(self):
        call = self._network_http_request("meta/usage")
        total_call = call["daily_usage"]
        remaining = call["daily_limit"] - call["daily_usage"]
        return total_call, remaining

    def get_device_types(self):
        if self._device_types is None:
            type_label = {}
            res = self._network_http_request("type/device/base")
            for i in res:
                type_id = i["id"]
                label_value = i["label"]
                type_label[type_id] = label_value
            self._device_types = type_label
        return self._device_types

    @property
    def get_all_agents(self):
        agent_list = self._network_http_request("agent")
        ret = []
        for agent in agent_list:
            licence_time = agent["licence"].get("expiration_time", None)
            still_valid = (
                licence_time is None
                or datetime.strptime(licence_time, "%Y-%m-%dT%H:%M:%S+%f:00")
                >= datetime.utcnow()
            )
            api_enabled = agent.get("access_right", {}).get("api_enabled", False)
            if still_valid and api_enabled:
                ret.append(agent)
            if not api_enabled:
                _logger.warning(
                    "Agent %s not processed (API not enabled)",
                    agent.get("display_name"),
                )

        return ret

    def banned_device_list(self, agent, banned_vendors_list):
        agent_id = agent.get("id")
        agent_name = agent.get("display_name")
        device_list = self._network_http_request(f"agent/{agent_id}/device")
        new_device_list = []

        for device in device_list:
            device["agent_name"] = agent_name
            device_vendor = device.get("vendor", "").lower()
            for banned_vendor in banned_vendors_list:
                if device_vendor.startswith(banned_vendor.lower()):
                    new_device_list.append(device)
                    break
        return new_device_list
