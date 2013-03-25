from WookieDb import *

db = WookieDb("localhost", "wookiedbtest", "wookiedbtest", "wookiedbtest")

db.select("a", "b", "c")
