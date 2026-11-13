# Direccionamiento IPv4 e IPv6

Seleccion del TP1 grupal de 2024. El [CSV IPv4](../labs/addressing/ipv4.csv) conserva las cinco redes de la tabla final del informe y explicita las cantidades de clientes. No se redistribuye la consigna completa.

| Red | Prefijo | Primer host | Ultimo host / gateway LAN | Broadcast | Clientes iniciales → con crecimiento |
| --- | --- | --- | --- | --- | --- |
| LAN1 | `10.20.15.0/26` | `10.20.15.1` | `10.20.15.62` | `10.20.15.63` | 30 → 51 |
| LAN2 | `10.20.12.64/27` | `10.20.12.65` | `10.20.12.94` | `10.20.12.95` | 12 → 21 |
| LAN3 | `10.20.7.128/25` | `10.20.7.129` | `10.20.7.254` | `10.20.7.255` | 50 → 85 |
| WAN A–B | `192.168.2.212/30` | `192.168.2.213` | `192.168.2.214` | `192.168.2.215` | Enlace punto a punto |
| WAN A–C | `192.168.2.232/30` | `192.168.2.233` | `192.168.2.234` | `192.168.2.235` | Enlace punto a punto |

En las LAN se reserva el ultimo host para el gateway. El crecimiento se calcula como `ceil(clientes_iniciales × 1.70)`. El verificador comprueba que entren esos clientes y el gateway, que el prefijo elegido sea suficiente y que el siguiente prefijo mas pequeno ya no alcance.

Estas redes pertenecen al ejercicio de direccionamiento; no son las mismas subredes del TP2 de ruteo.

## Ejemplos IPv6 revisados

El [CSV IPv6](../labs/addressing/ipv6.csv) conserva la idea de tres enlaces punto a punto del informe, reemplazando los prefijos originales por direcciones de documentacion:

| Enlace | Prefijo | Extremos |
| --- | --- | --- |
| WAN 1–2 | `2001:db8:1::/127` | `2001:db8:1::` y `2001:db8:1::1` |
| WAN 1–3 | `2001:db8:1::2/127` | `2001:db8:1::2` y `2001:db8:1::3` |
| WAN 2–3 | `2001:db8:1::4/127` | `2001:db8:1::4` y `2001:db8:1::5` |

`2001:db8::/32` esta reservado para documentacion, no es un prefijo privado ULA. Ver [RFC 3849](https://www.rfc-editor.org/rfc/rfc3849) y el uso de `/127` en enlaces punto a punto en [RFC 6164](https://www.rfc-editor.org/rfc/rfc6164).

La publicacion verifica aritmetica de direcciones y ausencia de solapamientos. No supone que se haya configurado ni probado conectividad IPv6 con estas nuevas direcciones.
