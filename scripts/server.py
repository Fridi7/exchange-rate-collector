import datetime
import logging
import time
import grpc
import api
import mongo_rw

from concurrent import futures
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient
from protos import exchange_pb2
from protos import exchange_pb2_grpc
from config import *


def plan():
    api.req(client)
    return


class Running:
    def __call__(self, count=10, sleep_time=timeout):
        sched.add_job(plan, 'interval', seconds=sleep_time, id='my_job')
        sched.start()
        return


def starting(x, name='plan'):
    job_list = {job.name: job for job in sched.get_jobs()}
    if name in job_list:
        return False
    else:
        sched.add_job(plan, 'interval', seconds=x, id='my_job')
        return True


def stopping():
    sched.remove_all_jobs()
    return


def change_time(t):
    try:
        n = int(t)
        if n < 1:
            return 'entered number is less than one'
        sched.remove_all_jobs()
        sched.add_job(plan, 'interval', seconds=t)
        print('oning')
        return
    except ValueError:
        return 'no number entered'


def latest_exchange(client, name, quantity):
    mongo_rw.mongo_login(client)
    return mongo_rw.mongo_read(mongo_rw.mongo_login(client), name, quantity)


class Collector(exchange_pb2_grpc.CollectorServicer):
     def ServiceUptime(self, request, context):
        toc = datetime.datetime.now()
        up_time = (toc - tic)
        logging.info("{}".format("Client requested uptime"))
        return exchange_pb2.UptimeReply(message='uptime: %s!' % up_time)

    def StopSignal(self, request, context):
        stopping()
        logging.info("{}".format("Stopping service"))
        return exchange_pb2.StopReply(message='service stopped')

    def StartSignal(self, request, context):
        if starting(15) == True:
            logging.info("{}".format("Starting service"))
            return exchange_pb2.StartReply(message='service started')
        else:
            logging.info("{}".format("Start request rejected - service already exist"))
            return exchange_pb2.StartReply(message='Service already exist')

    def ChangeTimeout(self, request, context):
        change_time(request.timeout)
        logging.info("{}".format("Change timeout on: {} seconds".format(str(request.timeout))))
        return exchange_pb2.ChangeTimeoutReply(message="timeout changed to {} seconds".format(request.timeout))

    def ExchangeRates(self, request, context):
        logging.info("{}".format("Currency rates requested and response sent"))
        return exchange_pb2.ExchangeRatesReply(message="exchange rates: \n {}".format(latest_exchange(client,
                                                                                                        request.name,
                                                                                                        request.quantity)))


class Serve:
    def __call__(self, count=10):
        logging.info("{}".format("Launch grpc service"))
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        exchange_pb2_grpc.add_CollectorServicer_to_server(Collector(), server)
        server.add_insecure_port('[::]:' + port)  # аутентификация без защиты
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    tic = datetime.datetime.now()
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    client = MongoClient(username=MongoLogin, password=MongoPassword, authSource='exchange_rate')
    # client = MongoClient()
    sched = BlockingScheduler()
    logging.basicConfig(format='[%(asctime)s.%(msecs)03d | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S',
                        level=logging.INFO)
    t1 = Thread(target=Serve(), daemon=True)
    t2 = Thread(target=Running(), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
