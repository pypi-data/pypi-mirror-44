# AMY Plugin

[Amy Assistant](http://amy-assistant.at)

Just import amy to write your plugin.

```py
from amy import Plugin, Instance, Message

class Messenger(FacebookClient, Instance):

    def onCreate(self, username):
        self.username = username

    def onAuth(self, token):
        FacebookClient.__init__(self, self.username, token)

    def onStart(self):
        FacebookClient.listen()

    def onStop(self):
        FacebookClient.stopListening()

    def myNewMessageFunc(message)
        unifiedMessage = Message()
            .setPlatform('messanger')
        #   .setUser(message['user'])
        #   ...
        Plugin.publishMessange(unifiedMessage.toDict())


def main():
    Messenger = Plugin('messenger', Messenger)


if __name__ == "__main__":
    main()

```
