import sys
from Crypto.Hash import MD4
from Crypto.Hash import MD5

mes = "Hello World!!"

h1 = MD4.new()
h1.update(mes.encode("utf-8"))
print("MD4:"+h1.hexdigest())


h2 = MD5.new()
h2.update(mes.encode("utf-8"))
print("MD5:"+h2.hexdigest())
