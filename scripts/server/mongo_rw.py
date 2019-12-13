from pymongo.errors import ServerSelectionTimeoutError


def mongo_login(client_auth):
    try:
        db = client_auth["exchange_rate"]
        return db
    except ServerSelectionTimeoutError:
        print('Mongo unreachable')
        return exit(1)


def mongo_write(db, valuta):
    collection = db["valutes"]
    collection.insert_one(valuta)


def mongo_read(db, name, quantity):
    valuta = []
    collection = db["valutes"]
    if name == 'all':
        for x in collection.find():
            valuta.append(x)
        return valuta
    else:
        for x in db.get_collection('valutes').find({"name": name}).limit(quantity):
            if x not in db.get_collection('valutes').find({"name": name}):
                print("çheking")
                return 'Requested currency not found'
            valuta.append(x)
        if not valuta:
            return 'Requested currency not found'
        return valuta
