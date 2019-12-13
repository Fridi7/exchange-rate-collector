db.createUser(
  {
    user: "collector",
    pwd: "123456",
    roles: [ { role: "readWrite", db: "exchange_rate" } ]
  }
)
