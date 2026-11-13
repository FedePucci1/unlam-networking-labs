# Analisis de trafico con Wireshark

Notas revisadas a partir del TP1 parte 2 grupal de 2024. El informe retenido analiza intercambios ICMP y el acceso a una aplicacion web. No se publica una captura `.pcap`/`.pcapng` ni se genero trafico nuevo para esta revision.

## Filtros de visualizacion

Los ejemplos usan una direccion de documentacion; hay que sustituirla por la direccion del host de un laboratorio propio o por un host presente en una captura autorizada.

| Objetivo | Filtro |
| --- | --- |
| Todo ICMPv4 | `icmp` |
| Echo request | `icmp.type == 8` |
| Echo reply | `icmp.type == 0` |
| ICMP en ambos sentidos de un host | `icmp && ip.addr == 198.51.100.10` |
| Solo paquetes hacia ese destino | `ip.dst == 198.51.100.10` |
| DNS | `dns` |
| TCP de un host, sin afirmar un protocolo de aplicacion | `tcp && ip.addr == 198.51.100.10` |
| Trafico TCP que involucra el puerto 443 | `tcp.port == 443` |

`ip.dst` selecciona el destino; no muestra por si solo las respuestas que vuelven desde ese host. Para observar ambos sentidos se usa `ip.addr`. Estos son filtros de visualizacion, no filtros de captura. Ver la [documentacion de filtros de Wireshark](https://www.wireshark.org/docs/man-pages/wireshark-filter) y la [referencia de campos ICMP](https://www.wireshark.org/docs/dfref/i/icmp.html).

## Que observar

- Emparejar solicitudes y respuestas ICMP por identificador y secuencia, verificando el intercambio de direcciones de origen y destino.
- Diferenciar las cabeceras Ethernet, IP y de transporte; la direccion MAC corresponde al salto local y no identifica necesariamente al destino IP remoto.
- Separar consultas/respuestas DNS del establecimiento de una conexion TCP. La presencia de DNS depende tambien del cache y del mecanismo de resolucion del cliente.
- Diferenciar una conexion TCP, un intercambio TLS y una respuesta HTTP. Una captura cifrada no permite leer el contenido de aplicacion solo por filtrar el puerto 443.

Las observaciones del informe son historicas. Los filtros se documentan como guia de analisis; no se afirma haberlos ejecutado de nuevo sobre una captura conservada, porque ese archivo de captura no esta presente en esta seleccion.
