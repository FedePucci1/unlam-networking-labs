# Review notes and validation boundaries

## Source selection

The three selected 2024 reports name Federico Pucci as a team member. Other folders include 2021 submissions and exam files naming different students; those were excluded. The publication uses selected results and three report screenshots, not the full teaching documents.

## Historical Packet Tracer snapshot

The saved `topology.pkt` is a base/intermediate state associated with TP2, not a complete saved version of every experiment shown in the report:

- Router1 serial `0/0/0` has `10.1.1.5/30`; Router2 serial `0/1/0` instead has `11.1.1.6/30`, so those physical neighbors are in different IPv4 subnets.
- The five extracted running configs do not contain completed RIP/OSPF process configuration, even though the report includes output from those experiments.
- Both PCs on Switch1 are initially assigned VLAN 30; both PCs on the multilayer switch are initially assigned VLAN 10. The reviewed plan moves one PC per switch to the other VLAN and documents new host settings.
- Some IPv6 settings in the snapshot differ from the report's later states. The reviewed overlays are explicitly IPv4-only and do not repair or validate the whole IPv6 configuration.

The original snapshot is preserved unchanged. It still includes built-in demonstration account/password fields from Packet Tracer. Decoded content was privately reviewed before publication; the raw XML is not published.

## Corrections and publication additions

| Issue | Published treatment |
| --- | --- |
| The report text gives OSPF an administrative distance of 120. | The reviewed notes distinguish the default values: OSPF 110, RIP 120. The retained OSPF screenshot itself shows `[110/...]`. See [Cisco's explanation](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html). |
| A destination-only display filter is described as if it showed both directions. | Packet-analysis notes use `ip.addr` for both directions and distinguish request/reply filters. |
| The snapshot cannot form the intended serial IPv4 adjacency. | The R2 overlay assigns `10.1.1.6/30`, matching the R1 peer's subnet. |
| ISP/server examples originally use arbitrary public address ranges. | Reviewed overlays use `198.51.100.0/27` and `203.0.113.0/30`, within [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737) documentation blocks. The historical file is unchanged. |
| The saved file lacks the demonstrated dynamic-routing states. | New overlays provide a documented OSPF IPv4 experiment, distinct from the saved historical artifact and screenshots. |

The overlays, CSV/JSON plans, verifier, topology diagram and Markdown notes were prepared during publication. They are not represented as verbatim historical submissions.

## What passed and what remains manual

Static checks validate five IPv4 rows, three IPv6 rows, capacity for LAN growth, non-overlapping subnets, three physical transit pairs, five host/gateway/VLAN assignments, default/return-route parameters and the native file hash. Optional native checks decode the file, compare all 11 objects and nine cables with the inventory and verify a byte-exact re-encoding.

These checks do not parse the complete IOS command language, boot network devices, establish OSPF neighbors, measure convergence, execute pings or reproduce packet captures. The command sequence and end-to-end forwarding require the [manual routing procedure](routing.md). No current successful simulator run is claimed.
