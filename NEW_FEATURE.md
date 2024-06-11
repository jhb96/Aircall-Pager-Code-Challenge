### SLACK CHANNEL INTEGRATION
Include now a Slack communcation channel (by a external system) to notify users by a channel and a url.

#### Implementation
To solve this, i consider to implement:

- New SlackTarget class that implements the ITarget interface.
- New SlackService class for the Slack integration adapter.
- Register the new SlackService in the ServiceLocator.
- Include a test that when an alert is notified with a SlackTarget in a policy, the SlackService is called with the correct parameters.
