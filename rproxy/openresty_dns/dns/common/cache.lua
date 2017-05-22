local _M = {}

local lrucache = require "resty.lrucache"

local local_cache = lrucache.new(5)  -- allow up to 5 items in the cache
if not local_cache then
    return error("failed to create the cache: " .. (err or "unknow"))
end

function _M.get(key)
    local value = local_cache:get(key)
    return value
end

function _M.set(key, value, exptime)
    if not exptime then
        exptime = 0
    end

    local_cache:set(key, value, exptime)
end

return _M
