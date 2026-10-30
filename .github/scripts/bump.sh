#!/bin/sh
# bump.sh <version>: point the add-on at Traefik Manager <version> and add a changelog entry.
set -eu
new=$1
old=$(sed -n 's/^version: "\(.*\)"$/\1/p' traefik_manager/config.yaml)
[ "$new" != "$old" ] || { echo "already $new"; exit 0; }
sed -i "s/^version: \".*\"$/version: \"$new\"/" traefik_manager/config.yaml
sed -i "s|ghcr.io/chr0nzz/traefik-manager:$old|ghcr.io/chr0nzz/traefik-manager:$new|" traefik_manager/build.yaml
grep -q "traefik-manager:$new" traefik_manager/build.yaml
{ printf '# Changelog\n\n## %s\n\n- Traefik Manager %s: https://github.com/chr0nzz/traefik-manager/releases/tag/v%s\n' "$new" "$new" "$new"
  tail -n +2 traefik_manager/CHANGELOG.md; } > CHANGELOG.new
mv CHANGELOG.new traefik_manager/CHANGELOG.md
echo "bumped $old -> $new"
