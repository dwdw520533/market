from rtconfig.client import RtConfigClient

client = RtConfigClient('market',
                        ws_url='ws://127.0.0.1:5015',
                        config_module=globals())
