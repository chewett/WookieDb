from WookieDb import *

db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")

r = db.query("show tables")

print r
