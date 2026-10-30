"""Start Traefik Manager with the add-on's options.

Traefik Manager reads most settings from the environment only on its first start; after that,
its manager.yml wins. So that the add-on configuration stays the source of truth, the options set
here are also written into manager.yml on every start (the client secret encrypted with Traefik
Manager's own key, as its UI would store it). Settings that are not add-on options stay editable
in the UI.
"""
import json
import os
import re
import sys

DATA = "/data"   # the add-on's persistent storage
SETTINGS = os.path.join(DATA, "manager.yml")

with open(os.path.join(DATA, "options.json")) as f:
    opts = json.load(f)

env = os.environ
env["SETTINGS_PATH"] = SETTINGS   # also puts the encryption key and caches in /data
env["BACKUP_DIR"] = os.path.join(DATA, "backups")
env["TRAEFIK_API_URL"] = opts["traefik_api_url"]
env["CONFIG_DIR"] = opts["dynamic_config_dir"]
env["COOKIE_SECURE"] = "true" if opts["cookie_secure"] else "false"
for key, name in (("static_config_path", "STATIC_CONFIG_PATH"),
                  ("acme_json_path", "ACME_JSON_PATH"),
                  ("access_log_path", "ACCESS_LOG_PATH")):
    if opts.get(key):
        env[name] = opts[key]
if opts.get("admin_password"):
    env["ADMIN_PASSWORD"] = opts["admin_password"]   # always wins over manager.yml
crowdsec = opts.get("crowdsec") or {}
if crowdsec.get("lapi_url"):
    env["CROWDSEC_LAPI_URL"] = crowdsec["lapi_url"]
if crowdsec.get("api_key"):
    env["CROWDSEC_API_KEY"] = crowdsec["api_key"]
for item in opts.get("env_vars") or []:   # anything else Traefik Manager reads, KEY=VALUE
    key, _, value = item.partition("=")
    env[key] = value

os.makedirs(env["BACKUP_DIR"], exist_ok=True)

oidc = opts.get("oidc") or {}
values = {
    "oidc_enabled": bool(oidc.get("enabled")),
    "oidc_provider_url": oidc.get("provider_url") or "",
    "oidc_client_id": oidc.get("client_id") or "",
    "oidc_client_secret": oidc.get("client_secret") or "",
    "oidc_display_name": oidc.get("display_name") or "SSO",
    "oidc_allowed_groups": oidc.get("allowed_groups") or "",
    "oidc_allowed_emails": oidc.get("allowed_emails") or "",
}
# First start: the environment seeds manager.yml.
for key, value in values.items():
    env[key.upper()] = ("true" if value else "false") if isinstance(value, bool) else value

if os.path.exists(SETTINGS):
    # Later starts: write the same values into manager.yml, with Traefik Manager's own code.
    sys.path.insert(0, "/app")
    from core import crypto   # noqa: E402  (uses SETTINGS_PATH for its key file)

    if values["oidc_client_secret"]:
        values["oidc_client_secret"] = crypto.encrypt_secret(values["oidc_client_secret"])
    with open(SETTINGS) as f:
        text = f.read()
    for key, value in values.items():
        line = f"{key}: {'true' if value else 'false'}" if isinstance(value, bool) else f"{key}: {json.dumps(value)}"
        text, n = re.subn(rf"^{key}:.*$", lambda _: line, text, count=1, flags=re.M)
        if n == 0:
            text += line + "\n"
    with open(SETTINGS, "w") as f:
        f.write(text)

os.chdir("/app")
cmd = ["/app/scripts/docker-entrypoint.sh", "gunicorn", "--config", "/app/gunicorn.conf.py", "app:app"]
os.execv(cmd[0], cmd)
