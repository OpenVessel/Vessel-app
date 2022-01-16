from flask_restful import abort

def abort_if_useraddr_doesnt_exist(userAddress, User):
    result = User.query.filter_by(userAddress=userAddress).first()
    if not result:
        abort(404, message="Could not find User Address")

def abort_if_userAddr_exists(userAddress):
    if userAddress in users:
        abort(409, message="UserAddress already exist")

# MetaMask Chain Id
# # Hex	Decimal	Network
# 0x1	1	Ethereum Main Network (Mainnet)
# 0x3	3	Ropsten Test Network
# 0x4	4	Rinkeby Test Network
# 0x5	5	Goerli Test Network
# 0x2a	42	Kovan Test Network