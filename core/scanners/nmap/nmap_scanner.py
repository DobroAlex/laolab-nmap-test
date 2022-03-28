from typing import Optional, Union

# TODO: importing style should be unified
import bs4
from bs4 import BeautifulSoup

from core.context import Context
from core.scanners.abstract_scanner import AbstractBaseScanner

import core.scanners.nmap.dataclasses as nmap_dataclasses
import core.scanners.nmap.utils as nmap_utils


class NmapScanner(AbstractBaseScanner):
    __report_root: Optional['BeautifulSoup'] = None

    def __init__(self, context: 'Context'):
        super().__init__(context)
        self.work_dir = context.program_args.output_file.parent

    @property
    def __get_report_as_soup(self) -> 'BeautifulSoup':
        report_file = self.context.program_args.output_file
        if not report_file.exists():
            raise RuntimeError(f'The report file at {report_file} doesnt exist')
        with report_file.open() as report:
            return BeautifulSoup(report.read(), 'lxml')

    @property
    def __get_report_root(self) -> 'BeautifulSoup':
        if self.__report_root:
            return self.__report_root

        if not (report_root := self.__get_report_as_soup.find('nmaprun')):
            raise RuntimeError(
                f'Cant find  "nmaprun" section within {self.context.program_args.output_file}'
            )
        # Sort of caching it to avoid constantly reading a file from disk
        self.__report_root = report_root
        return report_root

    @property
    def name(self) -> str:
        return 'Nmap scanner'

    @property
    def executable_path(self) -> str:
        return 'nmap'

    @property
    def cli_args(self) -> str:
        return f'-sV ' \
               f'-O ' \
               f'-oX {self.context.program_args.output_file} ' \
               f'{self.context.program_args.scan_target}'

    @property
    def is_return_code_ok(self) -> bool:
        if self.process.process.returncode != 0:
            return False
        if 'No targets were specified, so 0 hosts scanned' in self.process.stdout:
            return False
        return True

    def __get_meta_info(self) -> 'nmap_dataclasses.NmapRunMeta':
        report_root = self.__get_report_root
        run_start_meta_info = report_root
        run_finished_meta_info = report_root.find('finished')
        if not run_start_meta_info or not run_finished_meta_info:
            raise RuntimeError(f'Cant find run meta info')

        return nmap_dataclasses.NmapRunMeta(
            run_start_meta_info['scanner'],
            run_start_meta_info['args'],
            run_start_meta_info['start'],
            run_finished_meta_info['time'],
            run_start_meta_info['version'],
            run_start_meta_info['xmloutputversion'],
        )

    def __get_hosts_info(self) -> dict[str, tuple[bs4.element.Tag, nmap_dataclasses.Host]]:
        root = self.__get_report_root
        hosts: dict[str, tuple[bs4.element.Tag, nmap_dataclasses.Host]] = {}
        # TODO: These two for loops are not DRY
        #       (Although binning a new function can make it less readable)
        for host in root.find_all('host'):
            address_record: bs4.element.Tag = host.find('address')
            address = address_record['addr']
            address_type = address_record['addrtype']
            host_record = nmap_dataclasses.Host(address, address_type, [], None)
            hosts[address] = (host, host_record)
        return hosts

    @staticmethod
    def __get_closed_ports(markdown: bs4.element.Tag) -> list['nmap_dataclasses.Port']:
        all_closed_ports: list['nmap_dataclasses.Port'] = []
        closed_ports = markdown.find('extraports', {'state': 'closed'})
        for extra_reason in closed_ports.find_all('extrareasons'):
            reason: Optional[str] = extra_reason.get('reason')
            protocol: Optional[str] = extra_reason.get('proto')
            raw_ports: str = extra_reason.get('ports', '')
            all_ports: list[int] = []
            for port_group in raw_ports.split(','):
                if not port_group:
                    continue
                # Ports can be described as either single port or a group of ports delimited with a hyphen
                if '-' in port_group:
                    port_range_start = int(port_group.split('-')[0])
                    port_range_finish = int(port_group.split('-')[-1])
                    all_ports.extend(list(range(port_range_start, port_range_finish + 1)))
                else:
                    all_ports.append(int(port_group))

            for port in all_ports:
                all_closed_ports.append(
                    nmap_dataclasses.Port(
                        port,
                        protocol,
                        'closed',
                        reason,
                        None,
                        None,
                        None,
                        None,
                        None,

                    )
                )

        return all_closed_ports

    def __get_all_ports_info(
            self,
            markdown: bs4.element.Tag,
    ) -> list['nmap_dataclasses.Port']:

        open_ports = []
        all_reported_ports = markdown.find('ports')
        if all_reported_ports:
            reported_open_ports = all_reported_ports.find_all('port')
            for open_port in reported_open_ports:
                port_state: Union['bs4.element.Tag', dict] = open_port.find('state') or {}
                port_service: Union['bs4.element.Tag', dict] = open_port.find('service') or {}
                open_ports.append(
                    nmap_dataclasses.Port(
                        port_num=int(open_port['portid']),
                        protocol=open_port.get('protocol'),
                        # Assuming it's always 'open' but who knows
                        state=port_state.get('state'),
                        reason=port_state.get('reason'),
                        service_name=port_service.get('name'),
                        service_product=port_service.get('product'),
                        version=port_service.get('version'),
                        os_type=port_service.get('ostype'),
                        extra_info=port_service.get('extrainfo'),
                    )
                )
        closed_ports = self.__get_closed_ports(markdown)
        all_ports = open_ports + closed_ports
        all_ports.sort(key=lambda p: p.port_num)
        return all_ports

    def __get_os_version(
            self,
            markdown: bs4.element.Tag,
    ) -> Optional['nmap_dataclasses.OsVersion']:
        all_os_matches: list['nmap_dataclasses.OsVersion'] = []

        for os_match in markdown.find_all('osmatch'):
            for sub_version in os_match.find_all('osclass'):
                os_name = f'{sub_version.get("vendor", "")} {sub_version.get("os_gen", "")} {sub_version.get("osgen")}'
                accuracy = nmap_utils.get_os_version_accuracy(sub_version)
                all_os_matches.append(
                    nmap_dataclasses.OsVersion(
                        os_name,
                        accuracy,
                    )
                )
            os_name = os_match['name']
            accuracy = nmap_utils.get_os_version_accuracy(os_match)
            all_os_matches.append(
                nmap_dataclasses.OsVersion(
                    os_name,
                    accuracy,
                )
            )

        if not all_os_matches:
            return None
        all_os_matches.sort(key=lambda os_: len(os_.name), reverse=True)
        return max(all_os_matches, key=lambda os_: os_.accuracy)

    def parse_output(self):
        nmap_run_meta = self.__get_meta_info()
        hosts = self.__get_hosts_info()
        for host_ip, host_data in hosts.items():
            markdown, host = host_data
            host.ports = self.__get_all_ports_info(markdown)
            host.os_version = self.__get_os_version(markdown)

        return nmap_dataclasses.NmpRunReport(
            self.context.program_args.scan_target,
            self.context.program_args.output_file,
            nmap_run_meta,
            [host[1] for host in hosts.values()]
        )
