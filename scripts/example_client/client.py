from __future__ import print_function

import grpc
import logging

from protos import exchange_pb2
from protos import exchange_pb2_grpc
from config import *


def run(login):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = exchange_pb2_grpc.CollectorStub(channel)
    if login == "client":
        data = input(
            "Input command -> \n available command:\n ping (by default)\n change_timeout\n exchange_rates \n Exit")
        if data == "exchange_rates":
            name = input("Input currency (or 'all') ->")
            quantity = input("Input quantity ->")
            response = stub.ExchangeRates(exchange_pb2.ExchangeRatesRequest(name=name, quantity=quantity))
            print("Response: \n" + response.message)
        else:
            response = stub.ServiceUptime(exchange_pb2.UptimeRequest())
            print("Response: \n" + response.message)
    else:
        data = input(
            "Input command -> \n available command:\n ping (by default) \n stop\n start\n change_timeout\n "
            "exchange_rates")
        if data == "stop":
            response = stub.StopSignal(exchange_pb2.StopRequest())
            print("Response: \n" + response.message)
        if data == "start":
            response = stub.StartSignal(exchange_pb2.StartRequest())
            print("Response: \n" + response.message)
        if data == "change_timeout":
            time_out = int(input("input time period in seconds by number"))
            response = stub.ChangeTimeout(exchange_pb2.ChangeTimeoutRequest(timeout=time_out))
            print("Response: " + response.message)
        if data == "exchange_rates":
            name = input("Input currency (or 'all') ->")
            quantity = int(input("Input quantity ->"))
            response = stub.ExchangeRates(exchange_pb2.ExchangeRatesRequest(name=name, quantity=quantity))
            response_list = response.message.split('},')
            print("Response: \n" + '\n'.join(response_list))
        else:
            response = stub.ServiceUptime(exchange_pb2.UptimeRequest())
            print("Response: \n" + response.message)


def check():
    login = input("Enter login name: ")
    passw = input("Enter password: ")
    if login in users and users[login] == passw:
        print("\nLogin successful!\n")
        run(login)
    else:
        print("\nUser doesn't exist or wrong password!\n")
        exit(1)


if __name__ == '__main__':
    logging.basicConfig()
    check()
