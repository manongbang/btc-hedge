local string = string
local srv_resolver = require "common.srv_resolver"
local local_resolver = require "common.local_resolver"

function abort(reason, code)
    ngx.status = code
    ngx.say(reason)
    return code
end

local query_domain = ngx.var.srv_target
domain, port = query_domain:match("(.+):(%d+)")
if port then
    -- deal with link endpoint, like web:8000
    local ip = local_resolver.find_ip_by_host(domain)
    if ip then
        ngx.var.target = ip .. ":" .. port
    else
        return abort("[local] Unknown destination port", 500)
    end
else
    -- deal with srv endpoint, like web.domain.
    local target = srv_resolver.resolve_service(query_domain)
    if target then
        ngx.var.target = target
    else
        return abort("[dns service] Unknown destination port", 500)
    end
end
