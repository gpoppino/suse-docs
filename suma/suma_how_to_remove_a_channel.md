# How to remove a channel (clean up) from SUMA 3.x

This procedure describes how to remove or unsubscribe from a channel. It does
not delete it permanently. Only deletes its contents and synchronization status.

- Look for the channel name:

`# spacecmd softwarechannel_list`

- Remove the channel:

`# spacewalk-remove-channel -c channel_name`

- If the channel has subchannels, run instead:

`# spacewalk-remove-channel -a channel_name`

