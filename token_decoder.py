# This code shows approach to decode the token send to AWS API Gateway authorior

import base64
import json
from typing import List


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def decode_jwt_no_verify(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    payload_b64 = parts[1]
    payload = json.loads(b64url_decode(payload_b64))
    return payload


def extract_roles(payload: dict) -> List[str]:
    roles = set()

    # Realm roles
    realm_roles = payload.get("realm_access", {}).get("roles", [])
    roles.update(realm_roles)

    return sorted(roles)


if __name__ == "__main__":
    token = ""

    payload = decode_jwt_no_verify(token)

    user_info = {
        "name": payload.get("name"),
        "preferred_username": payload.get("preferred_username"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "email": payload.get("email"),
    }

    roles = extract_roles(payload)

    print("User Info")
    print("---------")
    for k, v in user_info.items():
        print(f"{k}: {v}")

    print("\nRoles")
    print("-----")
    for r in roles:
        print(f"{r}")
