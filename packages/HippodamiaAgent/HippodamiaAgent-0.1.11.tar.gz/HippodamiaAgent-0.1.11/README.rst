Hippodamia Agent
================

Reference implementation of an agent for the hippodamia microservice
montoring service. used by pelops.

It is unwise to set ``monitoring_agent.log-level`` to INFO or DEBUG if
``mqtt.log-level`` to INFO or DEBUG. As the mqtt\_client logs all
published messages to log-level INFO, this would result that the first
log-message that will be forwarded to the monitoring service will lead
to a log entry that this message has been publish. Which itself will
result in another message and another log entry and another message
forwarding this log entry ... to conclude as soon as the forwarding of
log-message with level INFO at MQTT log level INFO has been activated
the whole system is overloaded processing the first log message.

