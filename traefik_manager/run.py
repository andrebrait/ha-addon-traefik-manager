"""Start Traefik Manager with the add-on's options.

Traefik Manager reads most settings from the environment only on its first start; after that,
its manager.yml wins. So that the add-on configuration stays the source of truth, the OpenID
options are written into manager.yml on every start, through Traefik Manager's own settings code
(which encrypts the client secret and writes the file as its UI does). Settings that are not
add-on options stay editable in the UI.
"""
import json
import os
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
os.chdir("/app")
sys.path.insert(0, "/app")
from core import settings   # noqa: E402  (after SETTINGS_PATH is set: it decides where to write)

settings.update_settings(**values)

cmd = ["/app/scripts/docker-entrypoint.sh", "gunicorn", "--config", "/app/gunicorn.conf.py", "app:app"]
os.execv(cmd[0], cmd)
