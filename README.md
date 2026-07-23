# Operation FIRE STORM

## Your Mission

A critical situation has recently developed, and we’re calling on the brightest technical minds to assist. We're receiving incoming network transmissions from multiple unverified sources and need you to inspect and filter the stream for our operational team's sensitive data transmission.

Time is of the essence, and we need your expertise to rapidly handle this data before it’s too late. Your mission is to develop a high-speed program in **C, C++ or Rust** to intercept the network stream and extract the transmitted data while leaving everything else untouched, to keep our teams operating safely.

## Transmission Details

Unfortunately, we don't know the full details of the transmission protocol our operatives are using. You'll likely need to inspect the incoming data to work out the length of the header. Here's what we do know:

- Packets are incoming over **TCP** on port **5733** and non-operational data should be forwarded to port **5744**.
- The payloads of the packets when **placed in order** will form a PDF document. A PDF document begins with the string `%PDF`.
- The operation is running under the acronym "CTFS", packets of interest will start with this marker.
- The packet header includes a 2-byte **sequence number** as the first field followed by a 2-byte **length** value, both of which are in network order.
- You will likely need to inspect the traffic to find the length of the header. 

Your task is to forward the network data, while excluding the CTFS packets which should be used to reconstruct and store the transmitted document in the current directory.

### *Tips:* 
1. If you're stuck on where to start you could use [Wireshark](https://www.wireshark.org/) to inspect the network traffic on the pcap dump of the packet data (`test.py` could generate this for you). Alternatively, you could examine the received traffic using a live capture on loopback (`lo` interface).

2. When inspecting the traffic you'll need to work out the length of the CTFS packet's header. The first packet's payload should start with the PDF document marker!

## Operational Validation

Due to the importance of this operation succeeding, our analysts have captured some incoming traffic from the live environment and have written a Python file to replay the traffic to validate your solutions. 

This script is written for [**Python 3.12**](https://www.python.org/downloads/release/python-31213/) and will attempt to connect and send data to `localhost:5733`, and open a socket on `localhost:5744` to receive forwarded data, the script will validate that the right traffic is forwarded. You should also manually inspect the re-assembled document with a PDF reader to check the data has been received correctly.

To run the test, install and run `python`:

```bash
# Run your solution, and then in a separate terminal, run:
$ python test.py
```

If your solution passes the test "OK" should be printed to the screen.

If you would prefer to generate a `.pcap` file for packet analysis, we provide a `--pcap` switch:

```bash
$ python test.py --pcap

        (     (    (          (               )   (       *
        )\ )  )\ ) )\ )       )\ )  *   )  ( /(   )\ )  (  `
       (()/( (()/((()/( (    (()/(` )  /(  )\()) (()/(  )\))(
        /(_)) /(_))/(_)))\    /(_))( )(_))((_)\   /(_))((_)()\
       (_))_|(_)) (_)) ((_)  (_)) (_(_())   ((_) (_))  (_()((_)
       | |_  |_ _|| _ \| __| / __||_   _|  / _ \ | _ \ |  \/  |
       | __|  | | |   /| _|  \__ \  | |   | (_) ||   / | |\/| |
       |_|   |___||_|_\|___| |___/  |_|    \___/ |_|_\ |_|  |_|

Written to output.pcap
# Inspect `output.pcap` using tools like Wireshark
```

## LLM/AI Agent Statement

At CoreTech we appreciate that LLMs and AI agents have become a de facto tool for iterating on software designs. To that end, using an LLM or AI agent to assist you in understanding your solution, in soliciting immediate feedback on approach, and in general understanding language features in a greater detail, is permissible. 

The aim of the challenge, however, is to assess your personal understanding and technical ability, so we will ask in the submission form for a brief overview of how you've used AI/LLMs, if you have. In addition you will be asked to explain your solutions and design decisions behind using various constructs, language features and tools as part of the interview process. So ensure you understand what you're using!

## Terms and Conditions

- All submissions must be hosted using a public code-hosting service. If you're using a popular service like GitHub, please keep your repository private while the challenge is live and invite the [CoreTech Careers](https://github.com/coretech-careers) account to allow us to review your submission. Solutions can be made public after the submission deadline has passed.
- All submissions must be submitted through the [submission form](https://jobs.eu.lever.co/coretechsecurity/e460de72-72e2-4b21-86fc-5c4f3cb80a1f).
- All submissions must include a detailed README for building and verifying your solution.
- All submissions must build for Ubuntu 24.04 LTS.
- You may not use third-party libraries other than your chosen language's standard library.

Good Luck!