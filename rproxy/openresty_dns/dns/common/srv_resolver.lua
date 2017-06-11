local _M = {}

local ngx = ngx
local resolver = require "resty.dns.resolver"

function log(msg)
    ngx.log(ngx.ERR, msg, "\n")
end

function _M.resolve_service(query_domain)
    -- deal with srv endpoint, like web.domain.
    local dns = os.getenv("DNS")
    ip, port = dns:match("(.+):(%d+)")
    local nameserver = {ip, tonumber(port)}

    local dns, err = resolver:new{
        nameservers = {nameserver}, retrans = 2, timeout = 250
    }

    if not dns then
        log("failed to instantiate the resolver: " .. err)
        return nil
    end
    log("Querying " .. query_domain)
    local records, err = dns:query(query_domain, {qtype = dns.TYPE_SRV})

    if not records then
        log("failed to query the DNS server: " .. err)
        return nil
    end

    if records.errcode then
        -- error code meanings available in http://bit.ly/1ppRk24
        if records.errcode == 3 then
            log("DNS not found #" .. records.errcode .. ": " .. records.errstr)
            return nil
        else
            log("DNS error #" .. records.errcode .. ": " .. records.errstr)
            return nil
        end
    end

    if records[1].port then
        -- resolve the target to an IP
        local target_ip = dns:query(records[1].target)[1].address
        -- pass the target ip to avoid resolver errors
        return target_ip .. ":" .. records[1].port
    else
        log("DNS answer didn't include a port")
        return nil
    end
    return nil
end

return _M
