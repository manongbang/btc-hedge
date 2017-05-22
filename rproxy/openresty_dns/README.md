# openresty

## URL

btc-hedge/openresty:1.9-dns

## nginx config sample

```
env DNS;
env SERVER_ENDPOINT;

http {
    ...

    # lua_code_cache off;
    lua_package_path 'dns/?.lua;../lualib/resty/?.lua;;';

    ...

    server {
        listen 80;
        server_name sample_server;

        location / {
            set_by_lua_block $srv_target { return os.getenv("SERVER_ENDPOINT") }
            set $target '';
            access_by_lua_file dns/resolve.lua;

            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://$target;
        }
    }
}
```

## docker config

DNS: name server ip:port

SERVER_ENDPOINT: mesos service domain name (e.g. _redis.app_group._tcp.marathon.slave.mesos.)

