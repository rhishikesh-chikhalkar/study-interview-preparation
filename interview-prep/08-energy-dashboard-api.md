# Energy Dashboard API


08 — Energy Dashboard API

Snapshot

TA FastAPI service where | owned the security layer: a JWT verification middleware that validates O|

KTA/AuthO-issued bearer tokens against the identity provider's JWKS endpoint, plus a a
enforces role-based access from the token's group claims. It's the clean,

reusable auth pattern I use across FastAPI services.” :

STAR story — "Verify every token Properly, and gate endpoints by role" :

Situation. The service exposed portfolio/energy endpoints that must only be reachable

by authenticated users with the right roles — and token validation has to be done correctly (signature, expiry, audience, issuer), not just
there a token". E

Task. Implement robust JWT verification and declarative role-based access control.

Action.

Builta VerifyToken class using PyJWT with a PyJWKClient pointed at the IdP’s JWKS URL. For each request it extracts the kid from the token, fetches the matching signing key, and calls
validating signature, algorithm, audience, and issuer.

* Handled the real failure modes explicitly: expired signature, JWKS client errors,

decode errors, missing token — each mapped to a clear Unauthen ticated/ Unauthorized exception instead of a 500.
* Wrapped it in TokenVerificationMiddleware (Starlette BaseHTTPMiddleware ) with an excluded-paths allowlist (/, /api/public, does, /apenapi- Son) so health/docs stay o
* Added a roles_required dependency factory: it verifies the token, reads the groups claim, and raises 403 if none of the required roles are present — so protecting an endpoint is a one-line Dé}
* Configuration (issuer, audience, algorithms) via pydantic-settings, and structured logging with Loguru.

Result. A reusable, correct auth layer: endpoints are protected declaratively, tokens are fully validated against the IdP, and failures return precise 401/403 responses instead of leaking errors.

Technical deep-dive & why

Why JWKS instead of a shared secret? The IdP signs tokens with rotating asymmetric keys and publishes public keys at a JWKS endpoint. PyJWKClient fetches the right public key by”
signing secret, and key rotation on the IdP just works without redeploying.

© Why validate audience + issuer, not just signature? A signature-valid token issued for a different audience/app must be rejected. Checking aud and iss prevents token-reuse across services — a common ri 2al-
auth bug. Dei

* Why a dependency factory (roles_required("...") ) over inline checks? It's declarative and DRY: each endpoint states its required roles in its signature, and the check is centralised and testable. No copy-pasted
auth logic per route. Ly ;

* Why an excluded-paths list? Kubernetes probes hit /health//, and Swagger needs /docs + /openapi . json. Forcing auth on those breaks liveness checks and the docs Ul. i

* Why map exceptions explicitly? Auth errors must be 401 (who are you) vs 403 (not allowed) — not 500. Precise codes let clients react correctly and don’t leak internals.

Code samples (real, extracted from the repo)

Validate the JWT against the IdP's

JWKS — signature + exp + audience + issuer (app/security/token)

class VerifyToken:

verification middlewardé py, abridged)
def

and the check is centralised and testable. No copy-pasted

—_init__(self):

jwks_url = f"{settings.auth0 iss
self.jwks client =

PyIJWKClient(jwks_url)
async def verify(self,

# fetches + caches public keys by ‘kid’
if token is None:

token: HTTPAuthorizationCredentials) :
raise UnauthenticatedException
signing_key =

try:

# 401
self. jwks_client.get_signing_key_

from_jwt (token.credentials) .key
return jwt.decode(

token.credentials, signing key,
algorithms=settings.auth0_algorithms,
audience=settings.auth0_api_audience, 2
issuer=settings.auth0 issuer)

except jwt.ExpiredSignatureError:

: as i
raise UnauthorizedException( "Token has expired") “#40

Declarative per-endpoint RBAC from the token's groups claim ( app/security/rbac
def roles required(required_ roles: Str)? %
async def verify _role(token=Depends(HTTPBearer())):
auth_result = await auth.verify(token)
auth_result.get("groups", [])
if not any(role in user roles for role in required_roles):

user_roles =

raise HTTPException(status_code=403, detail="Access forbidden:
return auth_result

insufficient permissions")
# 403 — authenticated but not authorized

return verify_role

# usage:

@router.get("/data", dependencies=[Depends(roles_required(["FRG-Admins"]))] )

Likely follow-up Q&A

Q: Where does the JWKS client cache keys, and what if the ldP rotates keys? A: ‘PyJWKClient caches fetched signing keys; on an unknown kid it fetches fresh. So rotation is handled without redeploy. If the JWKS

endpoint is unreachable at startup | degrade safely (client is None — tokens are rejected as unauthorized father than crashing).

ed). 403 = valid token but the groups claim lacks a required role (roles_required).

Q: Difference between 401 and 403 in your code? A: 401 = nofinvalid/expired token (Unauthenticated

Authentication vs authorization, : :

Q: Middleware vs dependency — why both? A: The middleware enforces "must be authenticated" globally (with an allowlist). The roles_required dependency adds per-endpoint authorization. Global gate + fine-

grained gate.
Q: How would you test this without a real IdP? A: Generate tokens signed with a test key pair, point the JWKS client at a stub returning the public key, and assert: valid token — 200, expired — 401, wrong audience — 401.

missing role > 403.
