import logging
import time
from os.path import join, dirname

from .excel_writers import ExcelReport
from . import StringCell, AbstractCell, HyperLinkCell
from .api_wrapper import ApiWrapper

_logger = logging.getLogger('report')


class BanReporter:
    HEADERS_LABELS = (
        "ID",
        "agent_name",
        "Name",
        "Type",
        "Vendor",
        "IP Address",
        "MAC Address",
        "Last status",
        "First Seen(UTC Time)",
        "Last seen",
    )

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        file_name="FCC_Report",
        verbose=False,
    ):
        logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)
        if verbose:
            _logger.setLevel(logging.DEBUG)

        self.file_name = file_name
        self.wrapper = ApiWrapper(endpoint, api_key)

    def main_report(self):
        start = time.time()
        _logger.info("Starting report")
        builder = ExcelReport()

        file_name = self.file_name
        builder.create(file_name)
        _logger.debug("The Output file is created")
        row = builder.header(self._header_labels())
        _logger.debug("The Headers are specified")

        instructions = self._columns()
        _logger.debug("Columns are fetched to the output file")

        agent_list = self.wrapper.get_all_agents
        total_banned_devices_found = 0

        for agent in agent_list:
            device_list = self.wrapper.banned_device_list(agent, self._banned_vendors())
            total_banned_devices_found += len(device_list)
            _logger.info("Devices fetched for agent %s", agent.get("display_name"))
            for device in device_list:
                row = self._write_row(device, agent, instructions, row, builder)
        builder.close()
        _logger.info("File `%s.xslx` populated successfully", file_name)

        total_call, remaining = self.wrapper.api_call_counter()
        _logger.info("API Calls done for this report: %s", self.wrapper.count)
        _logger.info("Remaining daily API calls: %s", remaining)
        time_passed = time.time() - start
        _logger.info("Consumed time for preparation of the Report: %.2f s", time_passed)
        if total_banned_devices_found > 0:
            _logger.info("Found %s banned devices", total_banned_devices_found)
        else:
            _logger.info("Good news! No banned device found in your agents!")

    def _header_labels(self):
        ret = self.HEADERS_LABELS
        return ret

    def _columns(self):
        return (
            "id",
            "agent_name",
            self._display_name,
            self._type,
            "vendor",
            self._ip_addresses,
            "hw_address",
            "status",
            self._device_creation,
            "last_status_change",
        )

    def _write_row(self, device, agent_id, instructions, row, report):
        _logger.debug("Writing row %s for device %s", row, device["id"])
        for col, instruction in enumerate(instructions):
            try:
                value = instruction(device, agent_id)
            except TypeError:
                value = StringCell(device.get(instruction, ""))
            _logger.debug("Printing column %s - %s", col, str(instruction))
            report.write(row, col, value)

        return row + 1

    @staticmethod
    def _display_name(device, agent_id) -> AbstractCell:
        return HyperLinkCell(
            url=f"https://portal.domotz.com/webapp/#/agent/{agent_id}/devices/{device['id']}",
            label=device["display_name"],
        )

    def _type(self, device, *_) -> AbstractCell:
        type_id = device.get("type", {}).get("id")
        return StringCell(self._from_id_to_label(type_id) or "Generic")

    def _from_id_to_label(self, type_id):
        if type_id is None:
            return
        return self.wrapper.get_device_types()[type_id]

    @staticmethod
    def _ip_addresses(device, *_) -> AbstractCell:
        ip_list = device.get("ip_addresses")
        if ip_list:
            return StringCell(ip_list[0])
        return StringCell("")

    @staticmethod
    def _device_creation(device, *_) -> AbstractCell:
        return StringCell(device.get("first_seen_on", {}))

    def _banned_vendors(self):
        vendors = set()
        with open(
            join(dirname(__file__), "..", "banned_vendors.txt")
        ) as banned_vendors:
            for vendor in banned_vendors:
                vendor = vendor.strip()
                if vendor:
                    vendors.add(vendor)
        return vendors
