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
    
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI2aWYxUW9hVnBiUE84ZFJSdGR6YmhPdXZ2SzBuMzVNQ2hwSGU4UWZmQkdJIn0.eyJleHAiOjE3NzAwOTM5NDMsImlhdCI6MTc3MDA5MzY0MywianRpIjoiOTg2NmNlOWMtYTdhYi00OWU1LTg5NjMtOGExOWI1Y2RkODI5IiwiaXNzIjoiaHR0cHM6Ly8zLjEwNC4xMDkuMTY6ODQ0My9hdXRoL3JlYWxtcy9zd2Fuc3RlY2giLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNmZkMzRkNzItNzkwOC00ZjIyLTlmZWEtZmNmZTkxMGJlOWEyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6ImJlMDNkM2EzLTNlNDktNDU1YS1hOGVjLTQwMGM4YzFlNDdkZSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9tYWluLmQybmptYnphNjdhaXd2LmFtcGxpZnlhcHAuY29tIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJBdWRpdG9yIiwiRW5naW5lZXIiLCJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtc3dhbnN0ZWNoIiwiR2VuZXJhbCBNYW5hZ2VyIiwidW1hX2F1dGhvcml6YXRpb24iLCJTZWN1cml0eSBBZG1pbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6ImJlMDNkM2EzLTNlNDktNDU1YS1hOGVjLTQwMGM4YzFlNDdkZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkFkbWluIFN3YW5zIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW5Ac3dhbnN0ZWNoLmNvbS5hdSIsImdpdmVuX25hbWUiOiJBZG1pbiIsImZhbWlseV9uYW1lIjoiU3dhbnMiLCJlbWFpbCI6ImFkbWluQHN3YW5zdGVjaC5jb20uYXUifQ.NYuPmmt8mJDiY8G4VPeGP3h3-oPj0icxAIZ-BSfTMTA6aLM8FhFdGBsH40nF6apn44MhMy9UG_Fag21srqAficgWfv1zOmBCQ95uJs6o3BSGpcpO7h15jPwKR7dUVk6XFui1nac6azoTJw1oA_WmrGsmw_7n034KFB3k5R5jhxDn2pHb2IbRZTpnO7WfWw8at1bFqPYVY5wCvzW-dXSBiQTKVaVgD-Ue1wdGxuyuF9Li3PLadvtwspZ1Y1W24ec6IwOZDronNXggNqOXt5-bLJjM-irZDox78xbkVdrrtp-DselFkVf85JFTwJ8qS5IMjx5WZddHEqkO4EdZiXxlPA"  # input the token

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
