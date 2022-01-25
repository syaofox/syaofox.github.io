
```yaml
version: '2'

services:
  qbittorrent:
    image: linuxserver/qbittorrent:14.2.3.99202004172232-6962-29e9594ubuntu18.04.1-ls73
    container_name: qbittorrent
    restart: always
    networks: 
      macvlan:
        ipv4_address: 10.10.10.102
    environment:
      PUID: 1000
      PGID: 1000
      TZ: Asia/Shanghai
      UMASK_SET: 022
      WEBUI_PORT: 8080
    volumes:
      - /path/to/config:/config
      - /path/to/downloads:/downloads

networks:
  macvlan:
    name: macvlan
    driver: macvlan
    driver_opts:
      parent: ovs_eth0
    ipam:
      config:
        - subnet: 10.10.10.0/24
          gateway: 10.10.10.10
```
