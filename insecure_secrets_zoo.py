# insecure_secrets_zoo.py
# Purpose: intentionally expose many types of "secrets" to exercise code scanners.

import os
import json
import textwrap
import requests

# --- Classic API tokens / keys (regex-friendly shapes) ---
GITHUB_PAT = "ghp_a1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8s"  # ghp_ + 36 chars
SLACK_BOT_TOKEN = "xoxb-123456789012-123456789012-abcdefghijklmnopQRSTUVWX"
GOOGLE_API_KEY = "AIzaSyA1234567890abcdefGhijklmNOPQRstu"  # AIza + 35
STRIPE_SECRET = "sk_live_1234ABCD5678EFGH9012IJKL"          # sk_live_* style
TWILIO_ACCOUNT_SID = "AC0123456789abcdef0123456789abcdef"   # AC + 32 hex
TWILIO_AUTH_TOKEN = "abcdef0123456789abcdef0123456789"      # 32 hex

# --- Cloud creds / connection strings ---
AWS_ACCESS_KEY_ID = "AKIAABCD1234EFGH5678"                  # 20 chars
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"  # 40-ish
AZURE_STORAGE_CONNECTION = (
    "DefaultEndpointsProtocol=https;"
    "AccountName=demostorage;"
    "AccountKey=O1S2t3EXPOSED4u5v6w7x8y9z0A1B2C3D4E5F6G7H8I9J0K==;"
    "EndpointSuffix=core.windows.net"
)
MONGODB_URI = "mongodb+srv://demoUser:demoPass123@cluster0.example.mongodb.net/mydb?retryWrites=true&w=majority"
POSTGRES_URI = "postgresql://appuser:supersecret@db.example.com:5432/app"

# --- Bearer / Basic auth examples ---
BEARER_TOKEN = "sk_live_EXPOSED_DEMO_TOKEN_1234567890"
BASIC_USER = "admin@example.com"
BASIC_PASS = "P@ssw0rd123!"
BASIC_URL = f"https://{BASIC_USER}:{BASIC_PASS}@httpbin.org/basic-auth/{BASIC_USER}/{BASIC_PASS}"

# --- JWT (sample public test token shape) ---
JWT_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvbiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9."
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
)

# --- Private keys (headers trigger most scanners) ---
OPENSSH_PRIVATE_KEY = textwrap.dedent("""\
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAuDemoBase64PayloadThatLooksLikeAKeyButIsNotReal123456
7890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM+/==
-----END OPENSSH PRIVATE KEY-----
""")

RSA_PRIVATE_KEY_PEM = textwrap.dedent("""\
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxDemoBase64PayloadThatTriggersDetectorsButIsFake123456
abcdeFGHIJKLMNOpqrstUVWXYZ0123456789+/abcdeFGHIJKLMNOpq==
-----END RSA PRIVATE KEY-----
""")

# --- Firebase / Google service account JSON (with embedded PEM) ---
FIREBASE_SA = {
    "type": "service_account",
    "project_id": "demo-project",
    "private_key_id": "1234567890abcdef1234567890abcdef12345678",
    "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEFAFakeBase64KeyThatTriggersFinders12345==\\n-----END PRIVATE KEY-----\\n",
    "client_email": "firebase-adminsdk@demo-project.iam.gserviceaccount.com",
    "client_id": "123456789012345678901",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
}

# Optional: write secret-y files so scanners that read *files* (not runtime) will catch them
GENERATE_FILES = True

def leak_to_stdout():
    """Print some values (many scanners also look at code text; printing is just to mimic usage)."""
    print("Bearer token used:", BEARER_TOKEN[:12] + "…")
    print("GitHub PAT starts with:", GITHUB_PAT[:4])
    print("Slack token prefix:", SLACK_BOT_TOKEN.split('-')[0])
    print("AWS Access Key:", AWS_ACCESS_KEY_ID)
    print("Mongo URI:", MONGODB_URI.split('@')[1][:20] + "…")

def insecure_http_calls():
    """Make harmless calls to httpbin to prove execution (no real secrets sent)."""
    r1 = requests.get("https://httpbin.org/bearer", headers={"Authorization": f"Bearer {BEARER_TOKEN}"}, timeout=10)
    print("[bearer] httpbin status:", r1.status_code)

    r2 = requests.get(BASIC_URL, timeout=10)
    print("[basic] httpbin status:", r2.status_code)

def write_secret_files():
    """Create files that look sensitive; commit them to your test repo to trigger file-based scanners."""
    os.makedirs("secrets_demo", exist_ok=True)

    with open(".env", "w") as f:
        f.write(textwrap.dedent(f"""\
            # Intentionally insecure test .env
            GITHUB_TOKEN={GITHUB_PAT}
            SLACK_BOT_TOKEN={SLACK_BOT_TOKEN}
            GOOGLE_API_KEY={GOOGLE_API_KEY}
            STRIPE_SECRET={STRIPE_SECRET}
            TWILIO_ACCOUNT_SID={TWILIO_ACCOUNT_SID}
            TWILIO_AUTH_TOKEN={TWILIO_AUTH_TOKEN}
            AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}
            AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}
            AZURE_STORAGE_CONNECTION="{AZURE_STORAGE_CONNECTION}"
            JWT_TOKEN={JWT_TOKEN}
            MONGODB_URI="{MONGODB_URI}"
            POSTGRES_URI="{POSTGRES_URI}"
        """))

    with open("config.ini", "w") as f:
        f.write(textwrap.dedent("""\
            [default]
            api_key = AIzaSyA1234567890abcdefGhijklmNOPQRstu
            stripe_secret = sk_live_1234ABCD5678EFGH9012IJKL
            """))

    with open("settings.yml", "w") as f:
        f.write(textwrap.dedent("""\
            secrets:
              github_pat: ghp_a1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8s
              aws:
                access_key_id: AKIAABCD1234EFGH5678
                secret_access_key: wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY
        """))

    with open("id_rsa", "w") as f:
        f.write(OPENSSH_PRIVATE_KEY)
    os.chmod("id_rsa", 0o600)

    with open("private_key.pem", "w") as f:
        f.write(RSA_PRIVATE_KEY_PEM)

    with open("firebase-sa.json", "w") as f:
        json.dump(FIREBASE_SA, f, indent=2)

    print("Wrote: .env, config.ini, settings.yml, id_rsa, private_key.pem, firebase-sa.json")

if __name__ == "__main__":
    leak_to_stdout()
    if GENERATE_FILES:
        write_secret_files()
    try:
        insecure_http_calls()
    except Exception as e:
        print("HTTP demo failed (okay for scanners):", e)
