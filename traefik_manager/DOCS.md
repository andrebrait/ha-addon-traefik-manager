# Traefik Manager

[Traefik Manager](https://github.com/chr0nzz/traefik-manager) is a web UI for a Traefik instance:
routes, services, middlewares, certificates, logs and, optionally, CrowdSec decisions. This add-on
runs it next to a Traefik add-on and edits that Traefik's configuration files.

## Before you start

Traefik Manager edits Traefik's files and reads Traefik's API, so the Traefik add-on must:

- use configuration files that this add-on can reach: the add-on maps Home Assistant's `/config`
  (read-write), `/ssl` (read-only) and `/share` (read-write);
- use a **directory** for its dynamic configuration (file provider with `directory:`);
- expose its API on the internal add-on network, for example `api: {insecure: true}` on an entry
  point that is not published to the host. Add-ons reach each other by host name: an add-on with
  the slug `local_traefik` is `local-traefik`, one from a repository is `<repository id>-traefik`
  (shown on the add-on's page as "Hostname").

## Configuration

| Option | Description |
|---|---|
| `traefik_api_url` | Traefik's API, for example `http://local-traefik:8080` |
| `static_config_path` | Traefik's static configuration file, if Traefik Manager should show and edit it |
| `dynamic_config_dir` | Traefik's dynamic configuration directory; Traefik Manager writes its routes here |
| `acme_json_path` | Traefik's ACME storage, read-only, to show certificates |
| `access_log_path` | Traefik's access log, to show it |
| `cookie_secure` | Turn on when Traefik Manager is served over HTTPS (recommended) |
| `admin_password` | The admin password; always replaces the one stored by the UI |
| `oidc` | Login through an OpenID Connect provider (authentik, Keycloak, ...). Register the redirect URI `https://<your host>/auth/oidc/callback` with the provider. `allowed_groups` or `allowed_emails` must be set, or every login is refused |
| `crowdsec` | The CrowdSec LAPI URL and a bouncer key, to show and manage decisions |
| `env_vars` | Any other [Traefik Manager environment variable](https://traefik-manager.xyzlab.dev/env-vars.html), as `KEY=VALUE` |

The add-on writes the `oidc` options into Traefik Manager's settings on every start, so the
add-on configuration stays the source of truth for them (the UI's changes to those settings are
replaced at the next start). Everything else set in the UI is kept, in the add-on's own storage.

## Access

The web UI listens on port 5000 inside the add-on. Either:

- route a name to it through Traefik (recommended: TLS, and Traefik's IP allow lists and other
  middlewares apply), using the add-on's host name, for example `http://<repository id>-traefik-manager:5000`;
- or publish port 5000 in the add-on's Network settings. That serves plain HTTP: only on a
  trusted network.

Traefik Manager can change every route of your Traefik. Do not expose it to the internet.
