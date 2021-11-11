#! /usr/bin/env python
import logging
import asyncio

from py3tftp import file_io
from py3tftp.exceptions import ProtocolException
from py3tftp.protocols import TFTPServerProtocol, logger, RRQProtocol, \
    WRQProtocol, BaseTFTPProtocol
from py3tftp.cli_parser import parse_cli_arguments


class WRQROProtocol(WRQProtocol):
    def handle_initialization(self):
        self.set_proto_attributes()
        pkt = self.packet_factory.err_access_violation()
        self.send_opening_packet(pkt.to_bytes())
        self.handle_err_pkt()


class TFTPROServerProtocol(TFTPServerProtocol):
    def select_protocol(self, packet):
        logger.debug('packet type: {}'.format(packet.pkt_type))
        if packet.is_rrq():
            return RRQProtocol
        elif packet.is_wrq():
            return WRQROProtocol
        else:
            raise ProtocolException('Received incompatible request, ignoring.')

    def select_file_handler(self, packet):
        if packet.is_wrq():
            return lambda filename, opts: file_io.FileWriter(
                filename, opts, packet.mode)
        else:
            return lambda filename, opts: file_io.FileReader(
                filename, opts, packet.mode)


def main():
    args = parse_cli_arguments()

    logging.info('Starting TFTP server on {addr}:{port}'.format(
        addr=args.host, port=args.port))

    timeouts = {
        bytes(k, encoding='ascii'): v
        for k, v in vars(args).items() if 'timeout' in k
    }
    loop = asyncio.get_event_loop()

    listen = loop.create_datagram_endpoint(
        lambda: TFTPROServerProtocol(args.host, loop, timeouts),
        local_addr=(args.host, args.port,))

    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('Received signal, shutting down')

    transport.close()
    loop.close()


if __name__ == '__main__':
    main()
