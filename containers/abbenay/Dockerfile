# Abbenay AI daemon: gRPC-based LLM gateway for AI-assisted remediation.
# Downloads the pre-built binary from the GitHub release. Requires
# containers/abbenay/.env with LLM provider API keys at runtime.
FROM node:22-alpine

ARG ABBENAY_VERSION=v2026.3.6-alpha
ARG TARGETARCH=x64

WORKDIR /opt/abbenay

# Download and extract the release binary + proto files.
ADD https://github.com/redhat-developer/abbenay/releases/download/${ABBENAY_VERSION}/abbenay-${ABBENAY_VERSION#v}-linux-${TARGETARCH}.tar.gz /tmp/abbenay.tar.gz
RUN tar xzf /tmp/abbenay.tar.gz -C /opt/abbenay && rm /tmp/abbenay.tar.gz \
    && chmod +x /opt/abbenay/abbenay-daemon-linux-${TARGETARCH} \
    && ln -s /opt/abbenay/abbenay-daemon-linux-${TARGETARCH} /usr/local/bin/abbenay

COPY containers/abbenay/config.yaml /root/.config/abbenay/config.yaml

EXPOSE 50057

CMD ["abbenay", "daemon", "--grpc-host", "0.0.0.0", "--grpc-port", "50057"]
