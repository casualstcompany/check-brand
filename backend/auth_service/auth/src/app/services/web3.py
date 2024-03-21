from web3.auto import w3


class Web3Service:
    def __init__(self):
        return

    @staticmethod
    def validate_public_address(public_address: str):
        public_address = public_address.lower()
        return w3.is_address(public_address)


web3_service = Web3Service()
