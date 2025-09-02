# insecure_leak_only.py
# Intentionally INSECURE: for scanner testing only.

# Minimal fake secrets used by leak_to_stdout()
BEARER_TOKEN = "sk_live_EXPOSED_DEMO_TOKEN_1234567890"
GITHUB_PAT = "ghp_a1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8s"
SLACK_BOT_TOKEN = "xoxb-123456789012-123456789012-abcdefghijklmnopQRSTUVWX"
AWS_ACCESS_KEY_ID = "AKIAABCD1234EFGH5678"
MONGODB_URI = "mongodb+srv://demoUser:demoPass123@cluster0.example.mongodb.net/mydb?retryWrites=true&w=majority"

def leak_to_stdout():
    """Print some values (many scanners also look at code text; printing is just to mimic usage)."""
    print("Bearer token used:", BEARER_TOKEN[:12] + "…")
    print("GitHub PAT starts with:", GITHUB_PAT[:4])
    print("Slack token prefix:", SLACK_BOT_TOKEN.split('-')[0])
    print("AWS Access Key:", AWS_ACCESS_KEY_ID)
    print("Mongo URI:", MONGODB_URI.split('@')[1][:20] + "…")

if __name__ == "__main__":
    leak_to_stdout()
