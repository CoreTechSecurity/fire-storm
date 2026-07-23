"""Test Runner for FIRE STORM"""

import argparse
import struct
import time
import unittest
from pathlib import Path
from threading import Thread

from buffers import packets
from client import create_receiver, create_sender
from o import ps

parser = argparse.ArgumentParser(
    prog="fire-storm",
    description="Replay FIRE STORM test traffic",
)
parser.add_argument(
    "-p",
    "--pcap",
    help="Don't run tests interactively, instead dumps packet buffers to optional file name",
    required=False,
    const="output.pcap",
    default=None,
    nargs="?",
)
parser.add_argument(
    "-q",
    "--quiet",
    help="Remove ASCII art command line output",
    action="store_true",
)


class TestSolution(unittest.TestCase):
    data_received: dict[int, bytes] = {}

    def receive_msg(self, thread_id: int) -> None:
        receiver = create_receiver()

        try:
            while True:
                conn, _ = receiver.accept()
                conn_open = True
                while conn_open:
                    data = conn.recv(1024)

                    if len(data) == 0:
                        conn.close()
                        conn_open = False
                        break

                    if thread_id not in self.data_received:
                        self.data_received[thread_id] = b""
                    self.data_received[thread_id] += data

        except Exception:
            # print("Receiver thread - caught exception:", str(e))
            pass

        finally:
            receiver.close()

    def send_and_recv(self, packets: list[bytes], thread_count: int = 1):
        sender = create_sender()
        receiver_threads: list[Thread] = []

        for thread_id in range(thread_count):
            receiver_threads.append(Thread(target=self.receive_msg, args=(thread_id,)))
            receiver_threads[-1].start()

        time.sleep(1)
        for packet in packets:
            sender.sendall(packet)

        sender.close()

        for thread in receiver_threads:
            thread.join(timeout=5)

    def test_traffic(self):
        self.send_and_recv(packets.all)
        for i, packet in enumerate(packets.all):
            if i in packets.route1:
                self.assertIn(packet, self.data_received[0])
            if i in packets.route0:
                self.assertNotIn(packet, self.data_received[0])


def write_pcap_file(output: Path, packets: list[bytes]):
    with output.open("wb") as file:
        seconds = 1582675200
        file.write(struct.pack(">IHHIIIHH", 0xA1B2C3D4, 2, 4, 0, 0, 65536, 0, 1))
        for packet in packets:
            file.write(struct.pack(">IIII", seconds, 0, len(packet), len(packet)))
            file.write(packet)
            seconds += 1


if __name__ == "__main__":
    args = parser.parse_args()
    if not args.quiet:
        print("""
            (     (    (          (               )   (       *
            )\\ )  )\\ ) )\\ )       )\\ )  *   )  ( /(   )\\ )  (  `
        (()/( (()/((()/( (    (()/(` )  /(  )\\()) (()/(  )\\))(
            /(_)) /(_))/(_)))\\    /(_))( )(_))((_)\\   /(_))((_)()\\
        (_))_|(_)) (_)) ((_)  (_)) (_(_())   ((_) (_))  (_()((_)
        | |_  |_ _|| _ \\| __| / __||_   _|  / _ \\ | _ \\ |  \\/  |
        | __|  | | |   /| _|  \\__ \\  | |   | (_) ||   / | |\\/| |
        |_|   |___||_|_\\|___| |___/  |_|    \\___/ |_|_\\ |_|  |_|
        """)
    packets.all = ps(packets.all)
    if args.pcap is not None:
        write_pcap_file(Path(args.pcap), packets.all)
        print("Written to", Path(args.pcap))
    else:
        print("Running test...")
        unittest.main(exit=False)
