# AWS Certified Solutions Architect - Associate: EventBridge Study Notes

Current focus: Amazon EventBridge for SAA-C03 event-driven architecture questions.

## Exam Weight

EventBridge is most likely to appear in Domain 2: Design Resilient Architectures and Domain 4: Design Cost-Optimized Architectures. It can also appear in integration, decoupling, automation, operations, multi-account, and serverless workflow scenarios.

Key exam framing:

- Use EventBridge when you need event routing, filtering, fan-out, SaaS integration, scheduled invocation, or event-driven automation.
- Use event patterns to match only relevant events.
- Use rules to send matching events to one or more targets.
- Use EventBridge Scheduler for modern scheduled tasks.
- Use archive and replay when historical events must be reprocessed.
- Use SNS/SQS when the scenario is primarily messaging, buffering, or queue-based decoupling.

## Core EventBridge Concepts

Amazon EventBridge is a serverless event bus service for building event-driven applications. Producers publish events, EventBridge evaluates them against rules, and matching events are sent to targets.

EventBridge is useful when systems should be loosely coupled. Producers do not need to know which consumers exist, and consumers can be added later by creating more rules.

Primary EventBridge capabilities:

- Event buses: route events from many sources to many targets.
- Rules: match events or run on schedules.
- Targets: services, event buses, APIs, queues, functions, workflows, and other destinations.
- Scheduler: modern serverless scheduler for one-time and recurring invocations.
- Schemas: discover or define event structures and generate code bindings.
- Archives and replays: store selected events and resend them later.
- Pipes: point-to-point integrations from one source to one target with optional filtering, enrichment, and transformation.

## Event Buses

An event bus receives events and routes them to targets through rules. Rules are associated with a specific event bus, so a rule only evaluates events received by that bus.

Common event bus types:

- Default event bus: receives events from AWS services in the account.
- Custom event bus: used for your own applications, domains, or workloads.
- Partner event bus: receives events from supported SaaS partners.

Event buses can route events from:

- AWS services.
- Custom applications.
- SaaS partners.
- Other AWS accounts.
- Other event buses.

Exam rule: If the scenario says "route AWS service events or application events to multiple consumers based on event content," EventBridge event bus plus rules is usually the best answer.

## Events

An event is a JSON record describing a change, action, or state. AWS service events commonly include fields such as `source`, `detail-type`, and `detail`.

Example event pattern for EC2 running state:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

Important:

- EventBridge does not require consumers to poll the producer.
- A single event can match multiple rules.
- If an event matches no rules, EventBridge takes no action.
- Event patterns should be specific enough to avoid unnecessary target invocations.

## Rules

A rule defines what EventBridge does with events on an event bus.

Rule types:

- Event pattern rules: match incoming events based on JSON fields.
- Scheduled rules: legacy scheduled invocation capability.
- Managed rules: created and managed by AWS services for service functionality.

For event pattern rules:

- The rule matches event fields such as `source`, `detail-type`, or fields inside `detail`.
- A single rule can send events to multiple targets.
- Targets run in parallel.
- A rule can define input transformation before sending data to a target.

For scheduled needs:

- Prefer EventBridge Scheduler for new designs.
- Scheduled rules still exist, but AWS positions Scheduler as the more flexible and scalable service.

## Targets

A target is the destination that receives an event when a rule matches. A rule can define up to five targets.

Common targets:

- Lambda function.
- Step Functions state machine.
- SQS queue.
- SNS topic.
- Kinesis stream.
- ECS task.
- CodeBuild project.
- Systems Manager Automation or Run Command.
- API Gateway endpoint.
- AppSync API.
- Firehose delivery stream.
- Another event bus, including cross-account buses.
- API destination for external HTTPS endpoints.

Important permissions point:

- EventBridge needs permission to invoke or write to the target.
- Some targets use resource-based policies, such as Lambda permissions or SQS queue policies.
- Some targets require an IAM role that EventBridge can assume.
- If the target uses customer-managed KMS encryption, the KMS key policy may need to allow `events.amazonaws.com`.

Exam clue: If EventBridge cannot invoke a target, check target permissions, resource policy, execution role, and KMS key policy.

## Input Transformation

Input transformers reshape event data before delivery to the target.

Use input transformation when:

- The target only needs a subset of the event.
- The target expects a different JSON structure.
- You need to map event fields into a custom payload.
- You are sending events to an API destination or API Gateway endpoint.

Important:

- Input transformation changes what the target receives.
- Schema discovery infers the original event, not the transformed event.
- Keep transformations simple for exam scenarios unless the target explicitly requires a different shape.

## EventBridge Scheduler

EventBridge Scheduler is the preferred service for scheduled invocations. It supports recurring schedules and one-time schedules.

Use Scheduler for:

- Running a Lambda function every hour.
- Starting an ECS task every night.
- Sending an SQS message at a future time.
- Invoking AWS service APIs on a schedule.
- Creating millions of independent schedules.
- Using flexible time windows to distribute load.

Scheduler supports:

- `rate` expressions.
- `cron` expressions.
- One-time invocations.
- Flexible time windows.
- Retry configuration.
- Maximum retention time for failed invocations.
- Templated targets for common services.
- Universal targets for many AWS service API operations.

Exam rule: If a question asks for a modern, scalable way to run one-time or recurring tasks, choose EventBridge Scheduler over EventBridge scheduled rules.

## Archive and Replay

Archives store selected events from an event bus for later replay. You can filter which events are archived using an event pattern and configure retention.

Use archive and replay when:

- A target failed and historical events need to be reprocessed.
- You deploy a new consumer and want it to process previous events.
- You need to validate new functionality against historical production events.
- You need recovery from application processing errors.

Important limitations and reminders:

- An archive is tied to one source event bus.
- Archived events can only be replayed to the source event bus.
- Replaying events does not remove them from the archive.
- Replayed events include a `replay-name` field.
- Replay ordering is not guaranteed to be exactly the same as original event arrival order.
- Archive is not a general-purpose queue replacement.

Exam rule: If the scenario says "reprocess past events" or "recover by replaying previous events," choose EventBridge archive and replay.

## Schemas and Schema Registry

A schema defines the structure of events. EventBridge provides schemas for AWS service events, and you can create, upload, or infer custom schemas from events on an event bus.

Use schemas when:

- Developers need to understand event structure.
- Teams want strongly typed code bindings.
- You need to reduce errors when consuming event payloads.
- Multiple teams produce and consume custom events.

Important:

- EventBridge supports OpenAPI 3 and JSON Schema Draft 4.
- Schema discovery can infer schemas from events on a bus.
- Code bindings can be downloaded for supported programming languages.
- Do not confuse schemas with rules. Schemas describe event shape; rules route events.

## SaaS and Partner Integrations

EventBridge can receive events from supported SaaS providers through partner event sources.

Typical flow:

1. The SaaS partner creates a partner event source for your AWS account.
2. You associate that partner event source with a partner event bus.
3. The partner event bus becomes active.
4. You create rules on the partner event bus to route events to targets.

Important:

- Partner events published before association with an event bus are dropped.
- Partner event buses are tied to the partner event source.
- Common partner scenarios include monitoring, security, ticketing, CRM, ecommerce, and DevOps tools.

Exam clue: If a SaaS application needs to send events directly into AWS without custom polling or webhooks hosted by you, choose EventBridge partner integration when available.

## API Destinations

API destinations let EventBridge invoke HTTPS endpoints as rule or pipe targets.

Use API destinations when:

- A matching event should call an external SaaS API.
- You need to integrate with public or private HTTPS applications.
- You need EventBridge to manage authorization through a connection.
- The target is not an AWS service target.

Important:

- API destinations use connections for authorization and connectivity settings.
- Input transformers often shape the event to match the API contract.
- EventBridge retries some failures and can send undelivered events to a DLQ.
- API destinations are for outbound HTTP calls from EventBridge.

## EventBridge Pipes

EventBridge Pipes is for point-to-point event integration: one source, optional filtering or enrichment, and one target.

Use Pipes when:

- You need to connect one source to one target.
- You need filtering before invoking the target.
- You need enrichment before target delivery.
- You want less custom glue code between services.

Common pipe sources include streams and queues. Common targets include Lambda, Step Functions, SQS, EventBridge event buses, and other AWS services.

Exam distinction:

- Event bus: many sources to many targets, event routing and fan-out.
- Pipe: one source to one target, point-to-point flow with filtering/enrichment.

## Event-Driven Architecture Patterns

Event-driven design decouples producers from consumers.

Benefits:

- Loose coupling.
- Independent scaling of producers and consumers.
- Easier fan-out to multiple consumers.
- Easier addition of new consumers.
- Better integration across accounts, services, and teams.

Good EventBridge scenarios:

- Trigger workflow when EC2 instance changes state.
- Start a remediation Lambda when a security event occurs.
- Route order events to billing, fulfillment, and analytics consumers.
- Send SaaS events to AWS targets.
- Invoke scheduled operational tasks.
- Replay events after a failed deployment.

Common design checklist:

- Which event bus receives the events?
- Which event pattern matches the relevant events?
- Which targets should receive matching events?
- What permissions are needed for target invocation?
- Is target failure handled with retries or a DLQ?
- Do events need transformation?
- Do events need archiving for replay?
- Is ordering required? If yes, EventBridge may not be the right primitive by itself.

## EventBridge vs SNS

Both EventBridge and SNS can fan out messages, but they optimize for different cases.

Choose EventBridge when:

- You need content-based event routing with JSON event patterns.
- You need AWS service events or SaaS partner events.
- You need many event sources and many targets.
- You need archive and replay.
- You need schemas.
- You need event buses across accounts.

Choose SNS when:

- You need high-throughput pub/sub messaging.
- You need push fan-out to subscribers.
- You need mobile push, SMS, email, HTTP/S, SQS, Lambda, or Firehose subscribers.
- You need a simpler topic-based pub/sub model.

Exam shortcut:

- EventBridge: event routing and integration.
- SNS: pub/sub notification fan-out.

## EventBridge vs SQS

EventBridge and SQS solve different decoupling problems.

Choose EventBridge when:

- Events should be routed to one or more targets based on event content.
- Producers should emit events without knowing consumers.
- Multiple consumers may independently respond to the same event.
- You need AWS service, SaaS, or cross-account event integration.

Choose SQS when:

- You need a durable queue between one producer path and one consumer group.
- Consumers should poll and process messages at their own pace.
- You need buffering, backpressure handling, or load leveling.
- You need FIFO ordering or exactly-once processing semantics within FIFO constraints.
- You need a dead-letter queue for failed message processing.

Common pattern:

- EventBridge rule sends matching events to SQS.
- SQS buffers events for workers.
- Workers process messages reliably at their own pace.

Exam shortcut:

- EventBridge decides where events go.
- SQS holds work until consumers are ready.

## EventBridge vs Step Functions

Choose EventBridge when:

- You need to route events among systems.
- You need event-based fan-out.
- Systems react independently to changes.

Choose Step Functions when:

- You need an orchestrated workflow.
- Steps must run in a defined sequence.
- You need branching, retries, waits, error handling, or human approval logic.

Common pattern:

- EventBridge detects an event and starts a Step Functions state machine.
- Step Functions orchestrates the multi-step workflow.

## EventBridge vs CloudWatch Alarms

Choose EventBridge when:

- You react to events from AWS services, custom apps, or SaaS partners.
- You need event pattern matching and routing.

Choose CloudWatch Alarms when:

- You react to metric thresholds.
- You need alarm state transitions such as `OK`, `ALARM`, and `INSUFFICIENT_DATA`.

Common pattern:

- CloudWatch Alarm changes state.
- EventBridge captures the alarm state change event.
- EventBridge invokes a remediation target.

## Security and Permissions

Important security points:

- Use least privilege IAM roles for EventBridge target invocation.
- Use resource policies where required by the target.
- Use event bus policies for cross-account event publishing.
- Use KMS key policies when targets or buses use customer-managed keys.
- Use DLQs for failed target delivery where supported.
- Avoid putting sensitive data in events unless required and protected.

Cross-account event routing:

- The receiving account must allow events from the sending account or organization.
- Rules can target event buses in another account.
- Cross-account permissions are commonly controlled with event bus policies.

Exam clue: If a target uses SSE-KMS and EventBridge delivery fails, check whether the KMS key policy allows EventBridge to use the key.

## Reliability and Failure Handling

EventBridge is serverless and managed, but target delivery still needs design attention.

Use:

- Retry policies for temporary target failures.
- Dead-letter queues for undelivered events.
- Archives for replay and recovery.
- SQS targets when consumers need buffering or backpressure handling.
- Idempotent consumers because events may be delivered more than once.

Important:

- Design consumers to handle duplicate events.
- Do not assume strict ordering unless the target and architecture explicitly provide it.
- Use SQS FIFO when ordering is a hard requirement.

## Common Scenario Patterns

### AWS Service Event Triggers Lambda

Best answer: Create an EventBridge rule on the default event bus that matches the AWS service event and targets a Lambda function.

Why: AWS services publish events to the default event bus, and rules route matching events to targets.

### Multiple Consumers Need the Same Business Event

Best answer: Publish the event to a custom event bus and create separate rules for each consumer.

Why: EventBridge supports fan-out and loose coupling between producers and consumers.

### SaaS Events Need to Trigger AWS Workflows

Best answer: Use an EventBridge partner event source and partner event bus, then create rules targeting AWS services.

Why: Partner integrations avoid custom polling and reduce webhook infrastructure.

### Run a Task Every Day

Best answer: Use EventBridge Scheduler with a cron or rate expression.

Why: Scheduler is the modern service for centralized, scalable scheduled invocations.

### Run a Task Once in the Future

Best answer: Use EventBridge Scheduler one-time schedule.

Why: Scheduler supports one-time invocations without building custom delay logic.

### Reprocess Events After a Bug Fix

Best answer: Use EventBridge archive and replay.

Why: Archived events can be replayed to the source event bus for reprocessing.

### Buffer Events for Slow Consumers

Best answer: Use EventBridge rule target to SQS, then have consumers poll SQS.

Why: EventBridge routes events; SQS buffers work and provides backpressure handling.

### Need Ordered Processing

Best answer: Use SQS FIFO or another ordering-aware design, potentially as an EventBridge target.

Why: EventBridge is not primarily an ordered queue.

### Event Should Start a Multi-Step Workflow

Best answer: Use EventBridge to match the event and target Step Functions.

Why: EventBridge routes the triggering event; Step Functions orchestrates the workflow.

### External HTTPS API Must Be Called

Best answer: Use EventBridge API destination with a connection and input transformer.

Why: API destinations support outbound HTTPS targets with managed authorization configuration.

## Troubleshooting Checklist

When an EventBridge scenario is not working, check:

1. Is the event being sent to the expected event bus?
2. Does the rule belong to that event bus?
3. Does the event pattern match the actual event fields?
4. Is the rule enabled?
5. Is the target configured correctly?
6. Does EventBridge have permission to invoke or write to the target?
7. Does the target resource policy allow EventBridge?
8. Does the KMS key policy allow EventBridge if encryption is involved?
9. Is an input transformer producing valid payload for the target?
10. Are retries exhausted and events going to a DLQ?
11. Is a partner event source associated and active?
12. Is the target service or API returning errors or throttling?

## High-Yield Exam Reminders

- EventBridge is serverless.
- Event buses route events to targets through rules.
- The default event bus receives many AWS service events.
- Custom event buses are useful for application and domain events.
- Partner event buses receive SaaS partner events.
- Rules use event patterns to match event content.
- A rule can have up to five targets.
- A single event can match multiple rules.
- Targets run independently and in parallel.
- Use Scheduler for modern scheduled tasks.
- Scheduled rules are legacy compared with Scheduler.
- Use archive and replay to reprocess past events.
- Replayed events return to the source event bus.
- Schemas describe event structure and can generate code bindings.
- API destinations call HTTPS endpoints.
- Pipes are point-to-point; buses are many-to-many.
- EventBridge is not a queue replacement.
- Use SQS when buffering, backpressure, or FIFO ordering is required.
- Use SNS for simple pub/sub notification fan-out.
- Use Step Functions for workflow orchestration.
- Make consumers idempotent.
- Check IAM, resource policies, and KMS policies for target delivery failures.

## Practice Questions

### 1. EC2 State Change

An operations team wants to invoke a Lambda function whenever an EC2 instance enters the `stopped` state. What should be used?

Answer: Create an EventBridge rule on the default event bus that matches EC2 instance state-change events where the state is `stopped`, with Lambda as the target.

Why: AWS service events are delivered to the default event bus, and EventBridge rules route matching events.

### 2. SaaS Ticket Event

A company wants a ticketing SaaS platform to trigger a Step Functions workflow in AWS whenever a critical ticket is created. The company does not want to host webhook infrastructure. What is the best design?

Answer: Use an EventBridge partner event source and partner event bus, then create a rule that targets Step Functions.

Why: EventBridge partner integrations receive SaaS events directly and route them to AWS targets.

### 3. Daily Batch Job

A workload must start an ECS task every day at 1:00 AM. What should be used?

Answer: EventBridge Scheduler with a cron schedule targeting ECS.

Why: Scheduler is the preferred service for scalable scheduled invocations.

### 4. Reprocess Historical Events

After a bug fix, a team needs a new Lambda function to process events from the previous two days. What should have been configured?

Answer: EventBridge archive on the event bus, followed by replay for the required time window.

Why: Archive and replay lets selected historical events be resent to the source event bus.

### 5. Slow Consumer

An event-driven application receives bursts of order events. A downstream worker service must process every order but can only process a limited number at a time. What is the best target?

Answer: Send matching EventBridge events to an SQS queue and have workers poll the queue.

Why: EventBridge routes the events, while SQS provides buffering and load leveling.

### 6. Multiple Independent Consumers

An ecommerce platform publishes `OrderCreated` events. Billing, fulfillment, and analytics each need to process the same event independently. What is the best design?

Answer: Publish `OrderCreated` events to a custom EventBridge event bus and create rules for each consumer target.

Why: EventBridge supports loose coupling and fan-out based on event rules.

### 7. Ordered Processing

A financial workflow requires strict first-in, first-out processing of payment messages. What should be selected?

Answer: SQS FIFO, possibly as an EventBridge rule target if the events originate on an event bus.

Why: EventBridge is not primarily designed for strict ordered queue processing.

### 8. External REST API

An event should call an external HTTPS API after being filtered and reshaped. What EventBridge feature should be used?

Answer: API destination with a connection and input transformer.

Why: API destinations invoke HTTPS endpoints, and input transformers reshape the event payload.

### 9. Developers Need Event Structure

Several teams consume custom application events and want generated client code for event payloads. What should be used?

Answer: EventBridge schema registry and code bindings.

Why: Schemas define event structure and support generated bindings for development.

### 10. One Source to One Target With Enrichment

A queue message needs to be filtered, enriched with data from another service, and sent to one target without writing custom polling code. What should be considered?

Answer: EventBridge Pipes.

Why: Pipes are designed for point-to-point integrations with optional filtering and enrichment.

## Sources

- Amazon EventBridge overview: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html
- EventBridge event buses: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html
- EventBridge rules: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rules.html
- EventBridge targets: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html
- EventBridge Scheduler: https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html
- EventBridge archive and replay: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html
- EventBridge schemas: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html
- EventBridge SaaS integrations: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas.html
- EventBridge API destinations: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-destinations.html
- EventBridge Pipes: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html
