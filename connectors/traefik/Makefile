.PHONY: build-starter build-decision-service build-forwardauth-starter self-test self-test-decision-service self-test-forwardauth clean

build-starter:
	build/build-starter.sh build-starter

build-decision-service:
	build/build-starter.sh build-decision-service

build-forwardauth-starter: build-decision-service

self-test: self-test-decision-service

self-test-decision-service:
	build/build-starter.sh self-test-decision-service

self-test-forwardauth: self-test-decision-service

clean:
	build/build-starter.sh clean
