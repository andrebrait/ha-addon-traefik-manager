ARG BUILD_FROM
FROM ${BUILD_FROM}

COPY run.py /run.py

ENTRYPOINT ["python3", "/run.py"]

LABEL \
    io.hass.type="addon" \
    io.hass.name="Traefik Manager" \
    org.opencontainers.image.source="https://github.com/andrebrait/ha-addon-traefik-manager" \
    org.opencontainers.image.licenses="GPL-3.0"
