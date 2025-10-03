FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y bash net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
CMD ["bash"]