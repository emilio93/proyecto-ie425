| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 1 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 52715 → 5005 [SYN] Seq=0 Win=64240 Len=0 MSS=65495 WS=256 SACK_PERM=1 |

```
Frame 1: 66 bytes on wire (528 bits), 66 bytes captured (528 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 0, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 2 | 127.0.0.1 | 127.0.0.1 | TCP | 66 | 5005 → 52715 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=65495 WS=256 SACK_PERM=1 |

```
Frame 2: 66 bytes on wire (528 bits), 66 bytes captured (528 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 5005, Dst Port: 52715, Seq: 0, Ack: 1, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 3 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [ACK] Seq=1 Ack=1 Win=525568 Len=0 |

```
Frame 3: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 1, Ack: 1, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 4 | 127.0.0.1 | 127.0.0.1 | TCP | 58 | 52715 → 5005 [PSH, ACK] Seq=1 Ack=1 Win=525568 Len=4 |

```
Frame 4: 58 bytes on wire (464 bits), 58 bytes captured (464 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 1, Ack: 1, Len: 4
Data (4 bytes)

0000  68 6f 6c 61                                       hola
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 5 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 52715 [ACK] Seq=1 Ack=5 Win=525568 Len=0 |

```
Frame 5: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 5005, Dst Port: 52715, Seq: 1, Ack: 5, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 6 | 127.0.0.1 | 127.0.0.1 | TCP | 58 | 5005 → 52715 [PSH, ACK] Seq=1 Ack=5 Win=525568 Len=4 |

```
Frame 6: 58 bytes on wire (464 bits), 58 bytes captured (464 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 5005, Dst Port: 52715, Seq: 1, Ack: 5, Len: 4
Data (4 bytes)

0000  48 4f 4c 41                                       HOLA
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 7 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [ACK] Seq=5 Ack=5 Win=525568 Len=0 |

```
Frame 7: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 5, Ack: 5, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 8 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [FIN, ACK] Seq=5 Ack=5 Win=525568 Len=0 |

```
Frame 8: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 5, Ack: 5, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 9 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 52715 [ACK] Seq=5 Ack=6 Win=525568 Len=0 |

```
Frame 9: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 5005, Dst Port: 52715, Seq: 5, Ack: 6, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 10 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 5005 → 52715 [FIN, ACK] Seq=5 Ack=6 Win=525568 Len=0 |

```
Frame 10: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 5005, Dst Port: 52715, Seq: 5, Ack: 6, Len: 0
```

| No.     | Source                | Destination           | Protocol | Length | Info |
| ------- | --------------------- | --------------------- | -------- | ------ | ---- |
| 11 | 127.0.0.1 | 127.0.0.1 | TCP | 54 | 52715 → 5005 [ACK] Seq=6 Ack=6 Win=525568 Len=0 |

```
Frame 11: 54 bytes on wire (432 bits), 54 bytes captured (432 bits) on interface 0
Ethernet II, Src: 00:00:00_00:00:00 (00:00:00:00:00:00), Dst: 00:00:00_00:00:00 (00:00:00:00:00:00)
Internet Protocol Version 4, Src: 127.0.0.1, Dst: 127.0.0.1
Transmission Control Protocol, Src Port: 52715, Dst Port: 5005, Seq: 6, Ack: 6, Len: 0
```