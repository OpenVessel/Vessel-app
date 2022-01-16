
# MockUserData
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
user_put_args.add_argument("account_total", type=int, help="account_total Require", required=True)
user_put_args.add_argument("latest_month", type=int, help="latest_month Require", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
user_update_args.add_argument("account_total", type=int, help="account_total Require", required=True)
user_update_args.add_argument("latest_month", type=int, help="latest_month Require", required=True)

# EMFDeposit Validae Webrequest
EMFDeposit_put_args = reqparse.RequestParser()
EMFDeposit_put_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
EMFDeposit_put_args.add_argument("Deposit", type=int, help="Deposit Require", required=True)

# GET parse still not function TypeERROS
# EMFDeposit Validae Webrequest GET
EMFDeposit_get_args = reqparse.RequestParser()
EMFDeposit_get_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)

# EMFDeposit Validae Webrequest PATCH
EMFDeposit_patch_args = reqparse.RequestParser()
EMFDeposit_patch_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
EMFDeposit_patch_args.add_argument("Deposit", type=int, help="Deposit Require", required=True)

# EMFWithdraw Validate Webrequest
EMFWithdraw_get_args = reqparse.RequestParser()
EMFWithdraw_get_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)


# EMFDeposit Validae Webrequest
EMFWithdraw_put_args = reqparse.RequestParser()
EMFWithdraw_put_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
EMFWithdraw_put_args.add_argument("Withdraw", type=int, help="Deposit Require", required=True)

# ClaimDeposit Validate Web requesttt
# EMFDeposit Validae Webrequest
ClaimDeposit_put_args = reqparse.RequestParser()
ClaimDeposit_put_args.add_argument("userAddress", type=str, help="UserAddress Require", required=True)
ClaimDeposit_put_args.add_argument("Deposit", type=int, help="Deposit Require", required=True)

