# Sources, team attribution and publication changes

## 2024 reports

The following source documents explicitly list Federico Pucci as a student/team member:

| Local source, relative to UNLaM/Redes de computadoras | Published selection |
| --- | --- |
| `TP1/Parte 1/Resolucion.docx` | IPv4 subnet plan, growth-capacity review and IPv6 addressing notes |
| `TP1/Parte 2/Resolucion.docx` | Reviewed packet-analysis notes; raw captures and embedded desktop screenshots are not published |
| `TP2/Resolucion.docx` | Routing/VLAN analysis and three unchanged IOS-output screenshots |
| `TP2/topologia.pkt` | Unchanged historical base topology, extracted configs and inventory |

**TP1 team:** Facundo Carballo, Victor Povoli Olivera, Manuel Ruiz Diaz, Federico Pucci and Agustin Elias Gonzalez.

**TP2 team:** Facundo Carballo, Victor Povoli Olivera, Manuel Ruiz Diaz and Federico Pucci.

These are team submissions. The retained material does not establish individual ownership of every section, device configuration or screenshot. Course scenarios and initial topology scaffolding originate from the teaching material; the retained base `.pkt` is not claimed as a wholly original network design by Federico.

The 2021 group submissions and other named students' exam/lab files were excluded because their authorship evidence points to other people.

## Publication editions

Markdown explanations, CSV/JSON data, the verifier, CI, the Mermaid diagram and the five reviewed OSPF overlays were prepared during publication. They summarize, organize or correct selected coursework rather than reproducing the complete reports verbatim. The IPv6 point-to-point examples and the ISP/server overlay use documentation address prefixes.

The historical `.pkt` remains unchanged. Extracted configs normalize text line endings. Reviewed configuration changes are separate files and have not been executed in a simulator during this publication review.

| Public image | Embedded image in TP2/Resolucion.docx |
| --- | --- |
| `assets/r2-ripv2-protocols.png` | `word/media/image8.png` |
| `assets/r2-ospf-routes.png` | `word/media/image6.png` |
| `assets/r2-ripng-routes.png` | `word/media/image15.png` |

The three selected screenshots were visually reviewed and copied unchanged. Original report files, full course PDFs and unrelated student collections are not redistributed. Local source hashes are retained in the private publication audit; source documents were not edited.

## External tools and references

Native inspection used [packet-tracer-pkt-format](https://github.com/aacanadaa/packet-tracer-pkt-format), by aacanadaa, GPL-3.0-or-later. It is installed as an external dependency, not vendored or claimed as team-authored software. Cisco Packet Tracer itself is not distributed here.

Technical corrections cite primary Cisco, Wireshark and IETF documentation in the individual lab notes.
