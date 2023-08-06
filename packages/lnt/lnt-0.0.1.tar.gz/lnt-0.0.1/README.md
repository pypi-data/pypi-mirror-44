if RPC we must prepare the python gRPC client for Lightning Network

```
$ git clone https://github.com/googleapis/googleapis.git
$ curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
$ python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto
```

if not, then provide forwarded history and listchannel in json form and point via "--forwarded-payments" and "--channels".

Help of sort_routing_payments_by_channel.py

```
usage: sort_routing_channels.py [-h] [--rpc] [-st START_TIME] [-et END_TIME]
                                [-f FILE] [-c CHANNELS_F] [-t NUM_TO_PRINT]

optional arguments:
  -h, --help            show this help message and exit
  --rpc                 Uses gRPC to retrieve values instead of json
  -st START_TIME, --start_time START_TIME
                        Starting point of the forwarding history request in
                        UNIX timestamp. Required if --rpc
  -et END_TIME, --end_time END_TIME
                        End point of the forwarding history request in UNIX
                        timestamp. Required if --rpc
  -f FILE, --forwarded-payments FILE
                        Json file path of forwarded payments
  -c CHANNELS_F, --channels CHANNELS_F
                        Json file path of all channels for node
  -t NUM_TO_PRINT, --top NUM_TO_PRINT
                        Top x to return
```

### env variables that will be required by these tools

`MACAROON_PATH`	Path to admin.macaroon

`TLS_CERT_PATH` Path to tls.cert

`LND_URL` url for lnd node including port

`GRPC_SSL_CIPHER_SUITES`="HIGH+ECDSA"
