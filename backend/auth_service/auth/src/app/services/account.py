from typing import Optional

import eth_utils
from components.datastore import datastore
from config.config import config
from config.utils import create_nonce, session_scope
from eth_account.messages import defunct_hash_message
from models import LoginHistory, User
from services.user import user_service
from web3.auto import w3


class AccountService:
    def get_nonce(self, public_address: str) -> int:
        public_address = public_address.lower()

        if user := self.get_by_public_address(public_address):
            return user.nonce

        new_user = user_service.create_user_and_profile(
            public_address=public_address
        )

        return new_user.nonce

    def authentication(self, public_address: str, signature: str) -> bool:
        public_address = public_address.lower()
        user = self.get_by_public_address(public_address)

        if not user:
            return False
        message_hash = defunct_hash_message(
            text=config.AUTH.MESSAGE.format(nonce=user.nonce)
        )
        try:
            signer = w3.eth.account._recover_hash(
                message_hash, signature=signature
            )
        except eth_utils.exceptions.ValidationError:
            return False

        return signer.lower() == public_address

    @staticmethod
    def add_login_history(public_address: str, user_agent: str) -> None:
        public_address = public_address.lower()
        with session_scope() as session:
            login_history = LoginHistory(
                public_address=public_address, user_agent=user_agent
            )
            session.add(login_history)

    @staticmethod
    def get_by_public_address(public_address: str) -> Optional[User]:
        public_address = public_address.lower()
        return datastore.find_user(public_address=public_address)

    def change_nonce(self, public_address: str) -> None:
        if not config.LOCAL_MODE_TESTING:
            public_address = public_address.lower()
            with session_scope():
                user = self.get_by_public_address(public_address)
                user.nonce = create_nonce()


account_service = AccountService()
