from send import Send
from struct import pack

S = Send()
# print("CONNECT:", S.connect("45.249.49.168", 1234))
print("CONNECT:", S.connect("127.0.0.1", 1234))
S.run(0.1)
data = [True, 1, 1, True, 1, True, 1, 1, 1, True, 1, 1]
data_packed = pack("?Hh?H?Hhh?hh", *data)
S.change_data(data_packed)