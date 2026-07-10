.PHONY: build-connector build-traefik-connector build-forwardauth-service check-config check-traefik-config start-smoke start-smoke-traefik runtime-smoke runtime-smoke-traefik build-starter build-decision-service build-forwardauth-starter self-test self-test-decision-service self-test-forwardauth clean

build-connector:
	build/build-connector.sh

build-traefik-connector: build-connector

build-forwardauth-service: build-connector

check-config:
	scripts/check-config.sh

check-traefik-config: check-config

start-smoke:
	scripts/start-smoke.sh

start-smoke-traefik: start-smoke

runtime-smoke:
	scripts/runtime-smoke.sh

runtime-smoke-traefik: runtime-smoke

build-starter:
	build/build-starter.sh build-starter

build-decision-service:
	build/build-starter.sh build-decision-service

build-forwardauth-starter: build-connector

self-test: self-test-decision-service

self-test-decision-service:
	build/build-starter.sh self-test-decision-service

self-test-forwardauth: self-test-decision-service

clean:
	build/build-starter.sh clean
	build/build-connector.sh clean
