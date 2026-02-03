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
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI2aWYxUW9hVnBiUE84ZFJSdGR6YmhPdXZ2SzBuMzVNQ2hwSGU4UWZmQkdJIn0.eyJleHAiOjE3NzAwMTEwNTcsImlhdCI6MTc3MDAxMDc1NywianRpIjoiYjFlZGViN2MtNTQ5MC00MDY1LThmYTItYjgxYTIyZjA4NWQ5IiwiaXNzIjoiaHR0cHM6Ly8zLjEwNC4xMDkuMTY6ODQ0My9hdXRoL3JlYWxtcy9zd2Fuc3RlY2giLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNmZkMzRkNzItNzkwOC00ZjIyLTlmZWEtZmNmZTkxMGJlOWEyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6IjYzOTAyMWNmLWRhYzgtNGJhZi1hNDA5LTZkNDNiOTlhOGYzOSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9tYWluLmQybmptYnphNjdhaXd2LmFtcGxpZnlhcHAuY29tIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJBdWRpdG9yIiwiRW5naW5lZXIiLCJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtc3dhbnN0ZWNoIiwiR2VuZXJhbCBNYW5hZ2VyIiwidW1hX2F1dGhvcml6YXRpb24iLCJTZWN1cml0eSBBZG1pbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6IjYzOTAyMWNmLWRhYzgtNGJhZi1hNDA5LTZkNDNiOTlhOGYzOSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkFkbWluIFN3YW5zIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW5Ac3dhbnN0ZWNoLmNvbS5hdSIsImdpdmVuX25hbWUiOiJBZG1pbiIsImZhbWlseV9uYW1lIjoiU3dhbnMiLCJlbWFpbCI6ImFkbWluQHN3YW5zdGVjaC5jb20uYXUifQ.bwrCLgTZOTI0fqJXXE6U5Tlv0rvy61M2Uxf4mw24bLiHzWQlWQ2TGPRttfAICDQmZcxw0rpGjBvRSHsJVXVkEMh90JZfLaOB4E6uQAhzyTp0tm7oYbGIjFwnZ2qEL27nadxHG2XJ2AKViUF0_0tEFIXgi6GLgoiNgSIfCWxZ3fuZrXzp2HAa7A95ntNoyeeaosHxfsZcPV8E0nIATpZmjrVdUqIm_7Cr6RTU4Ywr2IHgik4-x707R7w4RICx-Bg8r1bWsO059PIqvlyNgcR8ogq57LIq4DWQo1vjIvoMQ_Pi6dLCeBF6XQQKcqVnfWYprj32UvuMgRwF3exgif95SA"

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
