lastkeys = nil
server = nil
ST_sockets = {}
nextID = 1

-- Definir los nombres de las teclas en el emulador.
local KEY_NAMES = { "A", "B", "s", "S", "<", ">", "^", "v", "R", "L" }

-- Detiene una conexión de socket por su ID.
function ST_stop(id)
	local sock = ST_sockets[id]
	ST_sockets[id] = nil
	sock:close()
	console:log("Socket " .. id .. " closed.")
end

-- Formatea mensajes para el log.
function ST_format(id, msg, isError)
	local prefix = "Socket " .. id
	if isError then
		prefix = prefix .. " Error: "
	else
		prefix = prefix .. " Received: "
	end
	return prefix .. msg
end

-- Maneja errores de socket.
function ST_error(id, err)
	console:error(ST_format(id, err, true))
	ST_stop(id)
end

-- Recibe mensajes de un socket y realiza acciones en el emulador.
function ST_received(id)
	local sock = ST_sockets[id]
	if not sock then return end
	while true do
		local p, err = sock:receive(1024)
		if p then
			console:log(ST_format(id, p))
			-- Interpretar el mensaje 'p' y enviar comandos al emulador.
			if p == "UP" then
				console:log('UP')
                emu:addKey(C.GBA_KEY.UP)
				emu:clearKey(C.GBA_KEY.UP)
            elseif p == "DOWN" then
                emu:addKey(C.GBA_KEY.DOWN)
            elseif p == "LEFT" then
                emu:addKey(C.GBA_KEY.LEFT)
            elseif p == "RIGHT" then
                emu:addKey(C.GBA_KEY.RIGHT)
            elseif p == "A" then
                emu:addKey(C.GBA_KEY.A)
            elseif p == "B" then
                emu:addKey(C.GBA_KEY.B)
            elseif p == "START" then
                emu:addKey(C.GBA_KEY.START)
            end
		else
			emu:clearKeys(0xF0)
			if err ~= socket.ERRORS.AGAIN then
				console:error(ST_format(id, err, true))
				ST_stop(id)
			end
			return
		end
	end
end

-- Escanea y envía estados de teclas.
function ST_scankeys()
	local keys = emu:getKeys()
	if keys ~= lastkeys then
		lastkeys = keys
		local msg = "["
		for i, k in ipairs(KEY_NAMES) do
			if (keys & (1 << (i - 1))) == 0 then
				msg = msg .. " "
			else
				msg = msg .. k;
			end
		end
		msg = msg .. "]\n"
		for id, sock in pairs(ST_sockets) do
			if sock then sock:send(msg) end
		end
	end
end

-- Acepta nuevas conexiones de socket.
function ST_accept()
	local sock, err = server:accept()
	if err then
		console:error(ST_format("Accept", err, true))
		return
	end
	local id = nextID
	nextID = id + 1
	ST_sockets[id] = sock
	sock:add("received", function() ST_received(id) end)
	sock:add("error", function() ST_error(id) end)
	console:log(ST_format(id, "Connected"))
end

-- Registro de callbacks y inicio del servidor.
callbacks:add("keysRead", ST_scankeys)

local port = 8888
server = nil
while not server do
	server, err = socket.bind(nil, port)
	if err then
		if err == socket.ERRORS.ADDRESS_IN_USE then
			port = port + 1
		else
			console:error(ST_format("Bind", err, true))
			break
		end
	else
		local ok
		ok, err = server:listen()
		if err then
			server:close()
			console:error(ST_format("Listen", err, true))
		else
			console:log("Socket Server Test: Listening on port " .. port)
			server:add("received", ST_accept)
		end
	end
end
