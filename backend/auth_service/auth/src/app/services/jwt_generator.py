from datetime import datetime
from typing import Optional

from config.cache import redis_db
from config.config import config
from config.utils import session_scope
from flask_jwt_extended import create_access_token, create_refresh_token
from models import AuthToken
from redis import Redis


class JWTGenerator:
    def __init__(self):
        self.model = AuthToken
        self.cache: Redis = redis_db

    def login(self, public_address: str, user_agent: str) -> tuple:
        public_address = public_address.lower()
        access, refresh = self._get_token_pair(public_address)
        self._add_or_update_refresh(public_address, user_agent, refresh)

        return access, refresh

    def _revoked_token(self, jti):
        key = f"revoked_token_{jti}"
        self.cache.set(key, "1", ex=config.JWT.ACCESS_EXPIRE)

    def refresh(
        self, public_address: str, user_agent: str, refresh_old: str
    ) -> Optional[tuple]:
        public_address = public_address.lower()
        access, refresh = self._get_token_pair(public_address)
        token = self._get_refresh_token(
            public_address=public_address,
            user_agent=user_agent,
            refresh_token=refresh_old,
        )
        if not token:
            return None
        with session_scope():
            token.refresh_token = refresh
        return access, refresh

    def logout(self, public_address: str, user_agent: str, jti: str) -> None:
        public_address = public_address.lower()
        self._revoked_token(jti)
        self._delete_refresh_token(public_address, user_agent)

    def full_logout(self, public_address) -> None:
        public_address = public_address.lower()
        key = f"full_logout_{public_address}"
        self.cache.set(
            key, datetime.now().timestamp(), ex=config.JWT.ACCESS_EXPIRE
        )
        self._delete_all_refresh_tokens(public_address)

    def _add_or_update_refresh(
        self, public_address: str, user_agent: str, refresh_token: str
    ) -> None:
        public_address = public_address.lower()
        token = self._get_refresh_token(public_address, user_agent)
        with session_scope() as session:
            if not token:
                token = self.model(
                    public_address=public_address, user_agent=user_agent
                )
                session.add(token)
            token.refresh_token = refresh_token

    def _get_refresh_token(
        self,
        public_address: str,
        user_agent: Optional[str] = None,
        refresh_token: Optional[str] = None,
        all_refresh: Optional[bool] = False,
    ) -> AuthToken:
        public_address = public_address.lower()
        params = {"public_address": public_address}

        if refresh_token:
            params["refresh_token"] = refresh_token
        if user_agent:
            params["user_agent"] = user_agent

        query = self.model.query.filter_by(**params)

        if all_refresh:
            return query.all()

        return query.first()

    def _delete_refresh_token(
        self, public_address: str, user_agent: str
    ) -> None:
        public_address = public_address.lower()
        with session_scope() as session:
            token = self._get_refresh_token(public_address, user_agent)
            if token:
                session.delete(token)

    def _delete_all_refresh_tokens(self, public_address: str) -> None:
        public_address = public_address.lower()
        with session_scope() as session:
            tokens = (
                self._get_refresh_token(public_address, all_refresh=True) or []
            )
            for token in tokens:
                session.delete(token)

    @staticmethod
    def _get_token_pair(public_address: str) -> tuple:
        public_address = public_address.lower()
        return create_access_token(
            identity=public_address
        ), create_refresh_token(identity=public_address)


jwt = JWTGenerator()
