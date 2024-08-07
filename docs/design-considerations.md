[toc]

# Design considerations

## Risks

- We removed a redundant LDAP check
before triggering the notification, the upstream script checks agains LDAP
that the user exists. This is also done by UMC and thus should be redundant.

## Why not use the upstream code?

The upstream code consists of three components,
which are deeply integrated with the UCS Appliance

- listener module
- cli script (executed by systemd)
  - uses UCR
  - systemd watchdog
  - cli arguments not needed
  - ldap call not needed
- UMC RPC client library
  - depends on UCR
  - Hard-Coded HTTPS
  - could not easily get it working

We would have to heavily patch these components to fit our stack
and the result would be much more complex than a reimplementation.

A complete rewrite based on the different features and constraints
of the Provisioning API was the better alternative.

## Authentication

- We use HTTP basic auth against UMC RPC on every request.
This is advantageous, becasuse we don't have to manage a UMC Session
including timeouts and reauthentication.
UMC creates only one session per user
meaning that even with thousands of requests including authentications
there is no risk of overloading the UMC Server with to many sessions.

## Retries

Scope:
The Selfservice Consumer is only responsible for a `umc-command` RPC request.
The UMC code ensures that a user actually exists and tries to send the email.
If the user does not exist or the mail address is invalid, it's a success
from the perspective of the Selfservice Consumer.

Only if the UMC responds with an error,
(because it can't reach it's mail gateway, internal server error, not found,)
it's a failure from the perspective of the Selfservice Consumer and should be retried.

The Provisioning API supports serverside retries.
But it currently only supports
infinite redelivery of the same message until it is acknowledged by the client.
If the Selfservice Consumer fails to handle a provisioning message
and trigger an email invitation, the container exits with an error code.
It will be redeployed by Kubernetes and retry the same message again.

Because of that limitation, the Selfservice Consumer
retries the same event forever until the UMC Server request is successful.
To unblock the Selfservice Consumer
the blocking message has to be manually deleted from the NATS queue.

In the future the Provisioning API should support a dead-letter queue
for failed messages. The Selfservice Consumer could then
put a message into this dead-letter queue
after a configurabe amount of retries.

The optimal behavour of the Provisioning API
from the perspective of the Selfservice Consumer would be
out-of-order redelivery with serverside exponential backoff.

This would give the Selfservice Consumer the opportunity
to try different messages instead of getting stuck,
retrying the same message forever.

The UMC Server RPC request is retried
with a configurable amount of times and exponential backoff
if the UMC Server is not reachable for any reason.
This handles temporary unavailability of the UMC Server more gracefully.
For example during an initial deployment or an upgrade scenario.
