from config.cache import redis_db


def check_token_in_cache(jwt_payload):
    jti = jwt_payload["jti"]
    user_id = jwt_payload["sub"]
    iat = jwt_payload["iat"]

    key_full_logout = f"full_logout_{user_id}"
    key = f"revoked_token_{jti}"

    full_logout = redis_db.get(key_full_logout)
    if full_logout and iat < float(full_logout):
        token_in_redis = True
    else:
        token_in_redis = redis_db.get(key)
    return token_in_redis is not None
