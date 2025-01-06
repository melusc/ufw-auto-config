# ufw-auto-config

Reconfigure UFW periodically from various sources (e.g. OpenAI IP ranges)

To reduce complexity there is minimal configuration. It is opinionated,
so it blocks e.g. OpenAI and you cannot disable this unless you modify the source code yourself.

## Configuration

See `./config.yml.sample`. Create `./config.yml`, set `allow.port`, `allow.ip`, `deny.port`, `deny.ip` as you desire.

Ports must be integers. Ports are passed to UFW as `ufw allow $PORT`

IPs can be IPv4 or IPv6 and can optionally be an IP range. Basically any IP that UFW accepts.
IPs are passed to UFW as `ufw allow from $IP`

## License

`ufw-auto-config` uses the GNU GENERAL PUBLIC LICENSE. See `./COPYING`.
