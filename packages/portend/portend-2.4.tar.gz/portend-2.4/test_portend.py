import socket
import contextlib

import pytest

import portend


def socket_infos():
	"""
	Generate addr infos for connections to localhost
	"""
	host = None  # all available interfaces
	port = portend.find_available_local_port()
	family = socket.AF_UNSPEC
	socktype = socket.SOCK_STREAM
	proto = 0
	flags = socket.AI_PASSIVE
	return socket.getaddrinfo(host, port, family, socktype, proto, flags)


def id_for_info(info):
	af, = info[:1]
	return str(af)


def build_addr_infos():
	params = list(socket_infos())
	ids = list(map(id_for_info, params))
	return locals()


@pytest.fixture(**build_addr_infos())
def listening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	sock = socket.socket(af, socktype, proto)
	sock.bind(sa)
	sock.listen(5)
	with contextlib.closing(sock):
		yield sa


@pytest.fixture(**build_addr_infos())
def nonlistening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	return sa


class TestChecker:
	def test_check_port_listening(self, listening_addr):
		with pytest.raises(portend.PortNotFree):
			portend.Checker().assert_free(listening_addr)

	def test_check_port_nonlistening(self, nonlistening_addr):
		portend.Checker().assert_free(nonlistening_addr)
