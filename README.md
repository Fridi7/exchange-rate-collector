# exchange rate collection service from the CBR in mongo using grpc

A service that collects information about the exchange rate of known currencies from the Central Bank of the Russian Federation xml at specified intervals. The collected data is stored in mongodb. 
Interval and authentication data for mongo are specified in the configuration file.
Messaging between the client and the management system is implemented using grpc.

## Installation

#### Installation requires
    
    $ ./requirements.sh
 
#### Generate proto
from directory protos:

    python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. exchange.proto
    
#### Running mongodb

    docker-compose up --build -d mongodb

## Usage

    ./server.py 
    ./client_example.py

##### The service processes the commands:
-     ping

the answer that the service is alive and functioning, transfers the service’s working time from launch
-     stop

  stop the API poll for updating the exchange rate
-     start

  resumes the survey
-     changeTimeout {timeout}

 change the timeout between API requests
-     exchangeRates {rate}, {quantity}

return n (quantity) of the last records from the database by currency (rate)

## Result example
for rate = "Евро" and quantity = 3:
 
![Image alt](https://github.com/Fridi7/exchange-rate-collector/blob/master/scripts/example_client/result%20example.png)
