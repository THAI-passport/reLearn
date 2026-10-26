FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential binutils file xxd gdb strace ltrace make git \
      python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# The labs target x86_64; on Apple Silicon hosts the container runs under emulation.
