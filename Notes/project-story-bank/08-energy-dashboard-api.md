# 08 — Energy Dashboard API

- **Repo**: `art-gh-frg-energy-dashboard-api`
- **Stack**: FastAPI, PyJWT, PyJWKClient, Pydantic-settings, Loguru, Starlette, EKS
- **Your Role**: Owned the security layer — JWT verification middleware and RBAC.

## Snapshot (30-second pitch)
"A FastAPI service where I owned the security layer: a JWT verification middleware that validates OKTA/Auth0-issued bearer tokens against the identity provider's JWKS endpoint, plus a `roles_required` dependency that enforces role-based access from the token's group claims. It's the clean, reusable auth pattern I use across FastAPI services."

---

## STAR Story — "Verify every token properly, and gate endpoints by role"

- **Situation**: The service exposed portfolio/energy endpoints that must only be reachable by authenticated users with the right roles — and token validation has to be done correctly (signature, expiry, audience, issuer), not just "is there a token".
- **Task**: Implement robust JWT verification and declarative role-based access control.
- **Action**:
  - Built a `VerifyToken` class using PyJWT with a `PyJWKClient` pointed at the IdP's JWKS URL. For each request it extracts the `kid` from the token, fetches the matching signing key, and calls `jwt.decode()` validating signature, algorithm, audience, and issuer.
  - Handled the real failure modes explicitly: expired signature, JWKS client errors, decode errors, missing token — each mapped to a clear `UnauthenticatedException`/`UnauthorizedException` instead of a 500.
  - Wrapped it in `TokenVerificationMiddleware` (Starlette `BaseHTTPMiddleware`) with an excluded-paths allowlist (`/`, `/api/public`, `/docs`, `/openapi.json`) so health/docs stay open.
  - Added a `roles_required` dependency factory: it verifies the token, reads the `groups` claim, and raises 403 if none of the required roles are present — so protecting an endpoint is a one-line `Depends`.
  - Configuration (issuer, audience, algorithms) via pydantic-settings, and structured logging with Loguru.
- **Result**: A reusable, correct auth layer: endpoints are protected declaratively, tokens are fully validated against the IdP, and failures return precise 401/403 responses instead of leaking errors.

---

## Technical Deep-Dive & Why

1. **Why JWKS instead of a shared secret?**
   - The IdP signs tokens with rotating asymmetric keys and publishes public keys at a JWKS endpoint. `PyJWKClient` fetches the right public key by `kid` — I hold no signing secret, and key rotation on the IdP just works without redeploying.

2. **Why validate audience + issuer, not just signature?**
   - A signature-valid token issued for a different audience/app must be rejected. Checking `aud` and `iss` prevents token-reuse across services — a common real-world auth bug.

3. **Why a dependency factory (`roles_required("...")`) over inline checks?**
   - It's declarative and DRY: each endpoint states its required roles in its signature, and the check is centralised and testable. No copy-pasted auth logic per route.

4. **Why an excluded-paths list?**
   - Kubernetes probes hit `/health`/`/`, and Swagger needs `/docs` + `/openapi.json`. Forcing auth on those breaks liveness checks and the docs UI.

5. **Why map exceptions explicitly?**
   - Auth errors must be 401 (who are you) vs 403 (not allowed) — not 500. Precise codes let clients react correctly and don't leak internals.

---

## Code Samples

### 1. Validate the JWT against the IdP's JWKS — signature + exp + audience + issuer (`app/security/token_verification_middleware.py`, abridged)
```python
class VerifyToken:
    def __init__(self):
        jwks_url = f"{settings.auth0_issuer}/.well-known/jwks.json"
        self.jwks_client = PyJWKClient(jwks_url)  # fetches + caches public keys by 'kid'

    async def verify(self, token: HTTPAuthorizationCredentials):
        if token is None:
            raise UnauthenticatedException  # 401

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token.credentials).key
            return jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.auth0_algorithms,
                audience=settings.auth0_api_audience,
                issuer=settings.auth0_issuer
            )
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token has expired")  # 401
```

### 2. Declarative per-endpoint RBAC from the token's groups claim (`app/security/rbac.py`)
```python
def roles_required(required_roles: list[str]):
    async def verify_role(token=Depends(HTTPBearer())):
        auth_result = await auth.verify(token)
        user_roles = auth_result.get("groups", [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=403,
                detail="Access forbidden: insufficient permissions"
            )  # 403 — authenticated but not authorized
        return auth_result
    return verify_role

# usage:
@router.get("/data", dependencies=[Depends(roles_required(["FRG-Admins"]))])
```

---

## Likely Follow-up Q&A

- **Q: Where does the JWKS client cache keys, and what if the IdP rotates keys?**
  - **A**: `PyJWKClient` caches fetched signing keys; on an unknown `kid` it fetches fresh. So rotation is handled without redeploy. If the JWKS endpoint is unreachable at startup, I degrade safely (client is None — tokens are rejected as unauthorized rather than crashing).

- **Q: Difference between 401 and 403 in your code?**
  - **A**: 401 = no/invalid/expired token (Unauthenticated). 403 = valid token but the `groups` claim lacks a required role (`roles_required`). Authentication vs authorization.

- **Q: Middleware vs dependency — why both?**
  - **A**: The middleware enforces "must be authenticated" globally (with an allowlist). The `roles_required` dependency adds per-endpoint authorization. Global gate + fine-grained gate.

- **Q: How would you test this without a real IdP?**
  - **A**: Generate tokens signed with a test key pair, point the JWKS client at a stub returning the public key, and assert: valid token → 200, expired → 401, wrong audience → 401, missing role → 403.
