# Simpleperf

## Introduction

Simpleperf is a streamlined variant of "iperf," which is a popular network testing tool. Its intuitive interface facilitates the measurement of network latency and bandwidth, making it a valuable resource for evaluating network performance across various scenarios.

## Installation and usage

Simpleperf is a versatile software tool that can function in two modes: client and server. By toggling between these modes, Simpleperf can either send or receive data as needed for the particular testing configuration.


To run simpleperf in client mode run `python3 simpleperf.py -c`

Optional client arguments:

| Short flag | Long flag  | Description                        | Default value | Required |
| ---------- | ---------- | ---------------------------------- | ------------- | -------- |
| -c         | --client   | Runs program as client             |               | true     |
| -I         | --serverip | Server ip adress                   | localhost     | false    |
| -t         | --time     | Durartion for data transfer        | 10 (seconds)  | false    |
| -p         | --port     | Server port                        | 8088          | false    |
| -f         | --format   | Print format                       | MB            | false    |
| -i         | --interval | Interval for data prints           | None (1)      | false    |
| -P         | --parallel | Create parallel client connections | None (1)      | false    |
| -n         | --num      | Size of data                       | 1000 bytes    | false    |


To run simpleperf in server mode run `python3 simpleperf.py -s`

Optional server arguments:

| Short flag | Long flag | Description            | Default value | Required |
| ---------- | --------- | ---------------------- | ------------- | -------- |
| -s         | --server  | Runs program as server |               | true     |
| -b         | --bind    | Custom server IP       | localhost     | false    |
| -p         | --port    | Custom server port     | 8088          | false    |
| -f         | --format  | Print format           | MB            | false    |

## Demo

Server:

<img width="750" alt="Screenshot 2023-03-23 at 15 22 49" src="https://user-images.githubusercontent.com/26365473/227233499-6dec022f-2f8e-4e0b-a57b-0f3201623c91.png">

Client:

<img width="796" alt="Screenshot 2023-03-23 at 15 23 12" src="https://user-images.githubusercontent.com/26365473/227233589-1b034c9f-b8e7-4648-82de-5f9b925882d2.png">
