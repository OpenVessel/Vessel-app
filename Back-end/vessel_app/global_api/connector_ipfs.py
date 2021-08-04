# https://github.com/ipfs-shipyard/py-ipfs-http-client
#p2p protocol 
import ipfshttpclient
res = client.add('test.txt')
res
{'Hash': 'QmWxS5aNTFEc9XbMX1ASvLET1zrqEaTssqt33rVZQCQb22', 'Name': 'test.txt'}
client.cat(res['Hash'])
'fdsafkljdskafjaksdjf\n'

# https://www.youtube.com/watch?v=bepuHIOGgOU&t=233s