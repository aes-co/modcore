from pyrogram import Client

def register(app: Client):
    from .etc import ban, kick, mute, unmute, warn, unwarn, warn_config, logchannel
    
    ban.register(app)
    kick.register(app)
    mute.register(app)
    unmute.register(app)
    warn.register(app)
    unwarn.register(app)
    warn_config.register(app)
    logchannel.register(app)
