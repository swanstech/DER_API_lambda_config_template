# this includes the authoriser lambda

import base64
import json
from typing import List, Dict, Any


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def decode_jwt_no_verify(token: str) -> Dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    payload_b64 = parts[1]
    payload = json.loads(b64url_decode(payload_b64))
    return payload


def extract_roles(payload: dict) -> List[str]:
    roles = set()

    # Realm roles (Keycloak standard)
    realm_roles = payload.get("realm_access", {}).get("roles", [])
    roles.update(realm_roles)

    return sorted(roles)


def generate_policy(principal_id: str, effect: str, resource: str, context: dict = None) -> dict:
    policy = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": resource
            }]
        }
    }

    # API Gateway requires ALL context values to be strings
    if context:
        policy["context"] = {k: "" if v is None else str(
            v) for k, v in context.items()}

    return policy


def lambda_handler(event, _context):
    """
    REST API Lambda Authorizer (TOKEN)
    Enforces: role must include 'General Manager'
    """
    try:
        auth = event.get("authorizationToken")
        if auth.startswith("Bearer "):
            token = auth[len("Bearer "):].strip()
        else:
            token = auth.strip()

        if not token:
            return generate_policy("anonymous", "Deny", event["methodArn"])

        payload = decode_jwt_no_verify(token)

        # Extract roles
        roles = extract_roles(payload)

        # DENY if role 'General Manager' is NOT present
        if "General Manager" not in roles:
            return generate_policy(
                principal_id="unauthorized",
                effect="Deny",
                resource=event["methodArn"]
            )

        # Extract user info (same as your local decoder)
        user_info = {
            "name": payload.get("name"),
            "preferred_username": payload.get("preferred_username"),
            "given_name": payload.get("given_name"),
            "family_name": payload.get("family_name"),
            "email": payload.get("email"),
        }

        context_out = {
            **user_info,
            "roles": ",".join(roles)
        }

        principal = (
            payload.get("preferred_username")
            or payload.get("email")
            or payload.get("sub")
            or "user"
        )

        # ALLOW only General Manager
        return generate_policy(
            principal_id=principal,
            effect="Allow",
            resource=event["methodArn"],
            context=context_out
        )

    except Exception:
        # Any error => deny
        return generate_policy(
            principal_id="unauthorized",
            effect="Deny",
            resource=event.get("methodArn", "*")
        )
