
FROM ghcr.io/siwatinc/python-baseimage:python3
ADD ./ /slcp_source
WORKDIR /slcp_source
RUN python3 setup.py install
RUN mkdir /config
WORKDIR /config
CMD cp -nv /slcp_source/config.json.example /config/config.json && \
    python3 -u -m siwat_remote_light_control_protocol_server