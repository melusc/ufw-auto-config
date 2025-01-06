# ufw-auto-config

Reconfigure UFW periodically from various sources (e.g. keep OpenAI IP ranges up to date to block)

To reduce complexity, there is minimal configurability.
If you do not want to block e.g. OpenAI, you have to modify the source code directly.

It always allows SSH as a fail-safe.

## Configuration

See `./config.yml.sample`. Create `./config.yml`, set `allow.port`, `allow.ip`, `deny.port`, `deny.ip` as you desire.

Ports must be integers. Ports are passed to UFW as `ufw allow/deny $PORT`

IPs can be IPv4 or IPv6 and can optionally be an IP range. Basically any IP that UFW accepts.
IPs are passed to UFW as `ufw allow/deny from $IP`

## License

`ufw-auto-config` uses the GNU GENERAL PUBLIC LICENSE. See `./COPYING`.
