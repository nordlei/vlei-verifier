FROM python:3.10-alpine as builder
WORKDIR /app

RUN apk update && apk add --no-cache alpine-sdk libffi-dev libsodium libsodium-dev bash && curl https://sh.rustup.rs -sSf | bash -s -- -y
COPY requirements.txt setup.py /app/
RUN mkdir /app/src
RUN source "$HOME/.cargo/env" && pip install -r requirements.txt


FROM python:3.10-alpine
WORKDIR /app

RUN apk update && apk --no-cache add bash alpine-sdk libsodium-dev
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app
COPY src/ /app/src/
COPY entrypoint.sh print_config.py /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]
