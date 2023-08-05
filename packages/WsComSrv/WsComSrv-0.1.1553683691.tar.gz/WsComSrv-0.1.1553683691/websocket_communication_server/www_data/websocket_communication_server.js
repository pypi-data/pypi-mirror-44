if(typeof logger === "undefined")
    logger = console;

var wscs={
    type_function:{'cmd':this.parse_socket_command},
    ws:null,
    cmd_functions:{"disconnect":function(data){this.ws.close()}.bind(this)},
    on_connect_functions:[],
    simple_message(sender, type="message", target="server", as_string=true, data=null) {
        m = {
            "type": type,
            "data": data,
            "from": sender,
            "target": Array.isArray(target)?target:[target],
        };
        if(as_string){
            return JSON.stringify(m);
        }
        return m
    },
    commandmessage(cmd, sender, target="server", as_string=true, args = [], kwargs={}){
        m = this.simple_message(
            sender,
            "cmd",
            target,
            false,
            data={"cmd": cmd, "args": args, "kwargs": kwargs},
        );
        if(as_string){
            return JSON.stringify(m);
        }
        return m
    },
    parse_socket_command(data) {
        var cmd = data.data;
        logger.debug('Command:', cmd);
        if(typeof this.cmd_function[cmd.cmd] !== "undefined"){
            this.cmd_function[cmd.cmd](data);
        }
        else logger.warn('Unknown command:',cmd.cmd);
    },
    websocket_connect(url) {
        this.ws = new WebSocket(url);
        this.ws.onopen = function() {
            for(let i=0;i<this.on_connect_functions.length;i++) {
                on_connect_functions[i]();
            }
        };

        this.ws.onmessage = function(e) {
            try {
                var data = JSON.parse(e.data);
                if(typeof this.type_function[data.type] !== "undefined")
                    this.type_function[data.type](data);
                else logger.warn('Unknown command type:', data.type, data);
            }catch(err) {
                logger.debug('Message:', e.data);
                logger.debug(err);
            }
        }.bind(this);

        this.ws.onclose = function(e) {
            logger.info('Socket is closed. Reconnect will be attempted in 10 second.', e.reason);
            setTimeout(function() {
                websocket_connect(url);
            }, 10000);
        };

        this.ws.onerror = function(err) {
            logger.error('Socket encountered error: ', err.message, 'Closing socket');
            this.ws.close();
        };
    },
    add_on_connect_function(ocf) {
        this.on_connect_functions.push(ocf)
    },
    add_cmd_funcion(name,callback){
        this.cmd_functions[name]=callback;
    },
    add_type_funcion(name,callback){
        this.type_function[name]=callback;
    },
};