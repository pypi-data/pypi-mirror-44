if (typeof logger === "undefined")
    logger = console;

var arduinocontrollserver = {
    global_t: 0,
    all_ports: {},
    update_ports(available_ports, connected_ports, ignored_port) {
        for (let port in this.all_ports) {
            this.all_ports[port].connected = false;
        }

        for (let i = 0; i < connected_ports.length; i++) {
            if (typeof this.all_ports[connected_ports[i]] === "undefined") {
                this.all_ports[connected_ports[i]] = {board_data: {}}
            }
            this.all_ports[connected_ports[i]].connected = true;
        }
        for (let port in this.all_ports) {
            if (!this.all_ports[port].connected) {
                //for(let j=0;j<portremovedfunctions.length;j++){portremovedfunctions[j](port);}
                delete this.all_ports[port];
            }
        }
    },
    boardupdate(data) {
        var board_data = data.data.kwargs.boarddata;
        if (typeof this.all_ports[board_data.port] === "undefined") return;

        for (let att in board_data) {
            this.all_ports[board_data.port].board_data[att] = board_data[att];
        }
    }
};

var acs = arduinocontrollserver;

$(function () {
    wscs.add_cmd_funcion("indentify", function () {
        wscs.ws.send(wscs.commandmessage(cmd = "indentify", sender = "gui", "server", true, [], {name: "gui"}))
    });
    wscs.add_cmd_funcion("set_time", function (data) {
        acs.global_t = data.data.kwargs.time
    }.bind(acs));
    wscs.add_cmd_funcion("set_ports", function (data) {
        acs.update_ports(data.data.kwargs.available_ports, data.data.kwargs.connected_ports, data.data.kwargs.ignored_port)
    }.bind(acs));
    wscs.add_cmd_funcion("boardupdate", acs.boardupdate);
    wscs.websocket_connect('ws://' + window.location.host + ':' + serverdata.socketport);
});
