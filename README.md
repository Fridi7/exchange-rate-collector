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

    python3 server.py 
    python3 client_example.py

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


### Available currencies

Доллар США, Евро, Австралийский доллар, Азербайджанский манат, Фунт стерлингов Соединенного королевства, Армянских драмов, Белорусский рубль, Болгарский лев, Бразильский реал, Венгерских форинтов, Гонконгских долларов, Датских крон, Индийских рупий, Казахстанских тенге, Канадский доллар, Киргизских сомов, Китайских юаней, Молдавских леев, Норвежских крон, Польский злотый, Румынский лей, СДР (специальные права заимствования), Сингапурский доллар, Таджикских сомони, Турецкая лира, Новый туркменский манат, Узбекских сумов, Украинских гривен, Чешских крон, Шведских крон, Швейцарский франк, Южноафриканских рэндов, Вон Республики Корея, Японских иен.
