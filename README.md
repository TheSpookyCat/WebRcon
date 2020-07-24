# WebRcon Package

## Install
`pip install webrcon`<br>
or<br>
`pip install https://github.com/lewdneko/webrcon/archive/master.zip`

## Docs

#### webrcon.RconConnector(host, port, password, message_callback=None, console_callback=None)
Initialises the class<br>
`host: str` - the IP/hostname of the server accepting WebRcon<br>
`port: Union[str, int]` - the port the server is accepting WebRcon on<br>
`password: str` - the password used to connect over WebRcon<br>
`message_callback: func` - a sync or async function that is called whenever a chat message is sent<br>
`console_callback: func` - a sync or async function that is called whenever a console message is sent<br>

##### <i>await</i> RconConnector.start(loop, **kwargs)
Opens a connection to the server<br>
`loop` - an asyncio event loop, can be obtained through asyncio.get_event_loop()<br>
`kwargs` - passed to websockets.client.connect - [read the docs](https://websockets.readthedocs.io/en/stable/api.html#websockets.client.connect)<br>

##### <i>await</i> RconConnector.close()
Closes the connection to the server

##### <i>await</i> RconConnector.command(command, callback)
Sends a command over RCON to the server<br>
`command: str` - The command you want to be sent to the server<br>
`callback: func` - A sync/async function that should take a single argument. The passed value will be a dict consisting of the output from the RCON server.<br>The response to your command will be under the `Message` key.

#### webrcon.InvalidServer
Your host/port/password combination is incorrect or the server isn't running.

#### webrcon.ConnectionClosed
You closed the connection and still tried to send a command. Good one.