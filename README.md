# Middle Where
A light-weight containerized HTTP API for running commands over ssh. Useful for running commands on the host of a machine, or two allow to containers to bridge networks and issue commands within a private network.

### Usage
```sh
curl -X POST \
    -H 'Content-Type: application/json' \
    -i http://localhost:5005/run \
    --data '{"host":"my-vps", "cmds": ["du -hs /root/backups"]}'

HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Mon, 23 Jul 2018 00:01:52 GMT
Connection: close
Content-Type: text/json; charset=utf-8
Content-Length: 214

{
    "host": "host",
    "cmds": ["du -hs /root/backups"],
    "responses": [
        {
            "cmd": "du -hs /root/backups",
            "output": "
                Command exited with status 0.
                === stdout ===
                4.8G    /root/backups

                (no stderr)"
        }
    ],
    "status": "success"
}
```

### The Guts

Middle Where uses a number of open source projects to work properly:

* *Flask* - Python3 Webserver running the basic HTTP API.
* *Fabric2* - SSH implementation for running remote commands.
* *Docker* - Containerized so it can deploy in a heart beat.
    * Apline Docker image so the install is minimal.

### Installation

To install, clone the repository, build the docker image, and run the docker service.

```sh
git clone https://github.com/politeauthority/middle-where.git
cd middle-where
docker build -t middle-where .
docker run \
    -v /home/root/middle-where-ssh:/root/.ssh \
    middle-where
```

### Todos

 - Add authentication
 - Add SSL support
 - Better logging

License
----

MIT
