FROM python:3.12-alpine

RUN apk update && apk add --no-cache alpine-sdk libffi-dev libsodium libsodium-dev bash && curl https://sh.rustup.rs -sSf | bash -s -- -y

WORKDIR /app
COPY requirements.txt setup.py /app/
RUN mkdir /app/src
RUN source "$HOME/.cargo/env" && pip install -r requirements.txt

COPY src/ src/
COPY entrypoint.sh print_config.py /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]
