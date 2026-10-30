# Traefik Manager add-on for Home Assistant

A Home Assistant add-on repository with one add-on: [Traefik Manager](https://github.com/chr0nzz/traefik-manager),
a web UI for the routes, services, middlewares and certificates of a Traefik instance, here the
Traefik add-on running on the same Home Assistant.

[![Add the repository to my Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fandrebrait%2Fha-addon-traefik-manager)

## Install

1. Settings → Add-ons → Add-on Store → ⋮ → Repositories, and add
   `https://github.com/andrebrait/ha-addon-traefik-manager` (or use the button above).
2. Install **Traefik Manager**, set its options (see the add-on's Documentation tab), and start it.

Home Assistant offers new versions as add-on updates. The add-on builds on Traefik Manager's own
image (`ghcr.io/chr0nzz/traefik-manager`), for `amd64` and `aarch64`.

## Releases

- Every pull request and push is linted, built and started (`lint.yml`).
- Every add-on version that reaches `main` without a release yet is checked again and published as
  `v<version>` (`publish.yml`): to release a change, bump `version` in `traefik_manager/config.yaml`
  and add a `CHANGELOG.md` entry in the pull request. The version follows Traefik Manager's; a change
  to the add-on alone adds a suffix (`1.15.4-1`, `1.15.4-2`, ...).
- Every day, `update.yml` checks for a new Traefik Manager release, applies it (`.github/scripts/bump.sh`),
  checks it, commits it to `main` and publishes it.
- Any failure while updating or publishing opens an issue assigned to the repository owner.

This is an add-on repository, not a HACS repository: HACS installs integrations and frontend
cards, while add-ons come from add-on repositories such as this one.

## License

GPL-3.0, as Traefik Manager. The icon is Traefik Manager's.
