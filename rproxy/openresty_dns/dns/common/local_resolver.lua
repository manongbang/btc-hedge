local _M = {}

local cache = require "common.cache"

function _M.find_ip_by_host(host)
    local chunks = {host:match("(%d+)%.(%d+)%.(%d+)%.(%d+)")}
    if #chunks == 4 then
        return host
    end
    local cache_key = 'HOST-' .. string.upper(host)
    local ip = cache.get(cache_key)
    if not ip then
        local file = io.open('/etc/hosts', 'r')
        for line in file:lines() do
            local index, obj = 1, {}
            for item in string.gmatch(line, '[^%s]+') do
                obj[index] = item
                index = index + 1
                if item == host then
                    ip = obj[1]
                    break
                end
            end
        end
        file:close()
    end
    if ip then
        cache.set(cache_key, ip)
    end
    return ip
end

return _M
