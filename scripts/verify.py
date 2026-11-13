"""Check address arithmetic, reviewed plan consistency and optional native archive integrity.

This is static validation, not IOS execution or a Packet Tracer simulation.
"""
import argparse
import csv
import hashlib
import ipaddress as ip
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_csv(path):
    with path.open(encoding='utf-8', newline='') as file:
        return list(csv.DictReader(file))


def disjoint(networks):
    for index, network in enumerate(networks):
        for other in networks[index + 1:]:
            assert not network.overlaps(other), f'Overlapping networks: {network}, {other}'


def addressing():
    rows = load_csv(ROOT / 'labs/addressing/ipv4.csv')
    networks = []
    for row in rows:
        network = ip.IPv4Network(row['network'])
        networks.append(network)
        assert str(network.netmask) == row['netmask']
        assert str(network.network_address + 1) == row['first_host']
        assert str(network.broadcast_address - 1) == row['last_host']
        assert str(network.broadcast_address) == row['broadcast']
        if row['gateway']:
            assert row['gateway'] == row['last_host']
            initial, future = int(row['initial_clients']), int(row['growth_clients'])
            assert future == math.ceil(initial * 17 / 10)
            assert network.num_addresses - 3 >= future  # network, broadcast, gateway reserved
            assert network.num_addresses // 2 - 3 < future  # smaller subnet would not fit
        else:
            assert network.prefixlen == 30
    disjoint(networks)
    rows6 = load_csv(ROOT / 'labs/addressing/ipv6.csv')
    networks6 = []
    for row in rows6:
        network = ip.IPv6Network(row['network'])
        networks6.append(network)
        assert network.prefixlen == 127 and network.subnet_of(ip.IPv6Network('2001:db8::/32'))
        assert ip.IPv6Address(row['endpoint_a']) == network.network_address
        assert ip.IPv6Address(row['endpoint_b']) == network.network_address + 1
    disjoint(networks6)
    print(f'PASS addressing: {len(rows)} IPv4 and {len(rows6)} IPv6 plans')


def interfaces(text):
    result = {}
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith('interface '):
            current = line.split(maxsplit=1)[1]
            result[current] = {}
        elif line in {'exit', 'end'} or line.startswith('router '):
            current = None
        elif current and line.startswith('ip address '):
            _, _, address, mask = line.split()
            result[current]['ip'] = ip.IPv4Interface(f'{address}/{mask}')
        elif current and line.startswith('switchport access vlan '):
            result[current]['vlan'] = int(line.split()[-1])
    return result


def physical_pair(a, b):
    return frozenset((tuple(a), tuple(b)))


def routing():
    folder = ROOT / 'labs/routing'
    plan = json.loads((folder / 'reviewed/plan.json').read_text(encoding='utf-8'))
    inventory = json.loads((folder / 'archive/inventory.json').read_text(encoding='utf-8'))
    aliases = plan['device_aliases']
    configs = {name: (folder / f'reviewed/{name}.cfg').read_text(encoding='utf-8') for name in aliases}
    parsed = {name: interfaces(text) for name, text in configs.items()}
    physical = {
        physical_pair((link['a']['device'], link['a']['port']), (link['b']['device'], link['b']['port']))
        for link in inventory['links']
    }
    used = []
    for link in plan['transits']:
        a, b = link['a'], link['b']
        left, right = ip.IPv4Interface(a[2]), ip.IPv4Interface(b[2])
        assert left.network == right.network and left.ip != right.ip
        assert physical_pair((aliases[a[0]], a[1]), (aliases[b[0]], b[1])) in physical
        for device, interface, address in [a, b]:
            actual = parsed[device][interface]['ip']
            assert actual == ip.IPv4Interface(address)
            used.append(actual.ip)
            if device != 'ISP' and 'ISP' not in {a[0], b[0]}:
                assert f'no passive-interface {interface}' in configs[device]
                assert f'network {actual.network.network_address} {actual.network.hostmask} area 0' in configs[device]
    assert len(set(used)) == len(used)
    for host in plan['hosts']:
        address = ip.IPv4Interface(host['ip'])
        gateway = ip.IPv4Address(host['gateway'])
        assert address.ip != gateway and gateway in address.network
        actual = parsed[host['gateway_device']][host['gateway_interface']]['ip']
        assert actual.ip == gateway and actual.network == address.network
        if 'vlan' in host:
            assert parsed[host['switch']][host['port']]['vlan'] == host['vlan']
            assert physical_pair((host['name'], 'FastEthernet0'), (aliases[host['switch']], host['port'])) in physical
            text = configs[host['gateway_device']]
            assert f'network {address.network.network_address} {address.network.hostmask} area 0' in text
    for device in ['R1', 'R2', 'MLS']:
        assert 'router ospf 10' in configs[device] and 'passive-interface default' in configs[device]
    assert 'ip routing' in configs['MLS']
    assert 'ip route 0.0.0.0 0.0.0.0 203.0.113.1' in configs['R1']
    assert 'default-information originate' in configs['R1']
    assert 'ip route 172.16.0.0 255.255.0.0 203.0.113.2' in configs['ISP']
    assert 'ip route 10.1.1.0 255.255.255.248 203.0.113.2' in configs['ISP']
    assert 'switchport trunk allowed vlan 30,40' in configs['SW1']
    print(f"PASS reviewed plan: {len(plan['transits'])} transit pairs and {len(plan['hosts'])} host/gateway/VLAN assignments")
    native = folder / 'archive/topology.pkt'
    assert hashlib.sha256(native.read_bytes()).hexdigest() == inventory['native_sha256']
    print('PASS historical native file SHA-256')
    return inventory, native


def native_archive(inventory, native):
    from pkt_core import decode, encode_bytes
    from pkt_core.models import Lab
    from pkt_core.export import to_netbox

    container = decode(native)
    assert encode_bytes(container.xml, container.format_name) == native.read_bytes()
    lab = Lab.from_bytes(container.xml)
    assert lab.version == inventory['saved_version']
    actual_devices = {d.name: (d.kind, d.model) for d in lab.devices}
    assert actual_devices == {d['name']: (d['kind'], d['model']) for d in inventory['devices']}
    exported = json.loads(to_netbox(lab))
    actual_links = {physical_pair((c['a']['device'], c['a']['port']), (c['b']['device'], c['b']['port'])) for c in exported['cables']}
    expected_links = {physical_pair((c['a']['device'], c['a']['port']), (c['b']['device'], c['b']['port'])) for c in inventory['links']}
    assert actual_links == expected_links
    assert len(lab.devices) == 11 and len(lab.links) == 9
    print('PASS native decode/encode round trip: 11 devices and 9 cable links')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', action='store_true', help='Also decode the archive with the optional pinned dependency')
    args = parser.parse_args()
    addressing()
    inventory, native = routing()
    if args.native:
        native_archive(inventory, native)
    print('Static checks passed. IOS execution, routing convergence and live packet forwarding are not tested here.')
