# Robot Framework Listeners

Robot Framework Listeners allow you to intercept and react to events during test execution. They are a powerful way to customize test logging, reporting, and overall behavior by executing custom Python code when tests start, end, or when specific events occur.

---

## Overview

Listeners are implemented as Python classes or modules that can be registered with Robot Framework. Once registered, a listener receives notifications for events such as:

- **start_suite / end_suite:** When a test suite begins or ends.
- **start_test / end_test:** When a test case begins or ends.
- **start_keyword / end_keyword:** When a keyword begins or ends.
- **log_message:** When a log message is created.

These event methods allow you to perform custom actions like writing to external logs, modifying test data, or integrating with other tools.

---

## When to Use Listeners

Listeners are useful for:
- Custom logging or reporting (e.g., generating HTML reports, sending notifications).
- Integrating with CI/CD pipelines.
- Tracking test progress or performance.
- Performing additional actions (e.g., cleanup, dynamic configuration) at specific points in the test run.

---

## Implementing a Listener

To create a listener, define a Python class with methods corresponding to the events you wish to handle. The listener must also define a class variable `ROBOT_LISTENER_API_VERSION` (currently, version 3 is recommended).

### Example Implementation

```python
class MyListener:
    ROBOT_LISTENER_API_VERSION = 3

    def start_test(self, data, result):
        print(f"Starting test: {data.name}")

    def end_test(self, data, result):
        print(f"Ending test: {data.name} with status {result.status}")
```

In this example:
- The `start_test` method is called before a test case starts.
- The `end_test` method is called after a test case finishes, where `result.status` indicates the test outcome.

---

## Registering a Listener

You can register a listener when running your Robot Framework tests using the command line. For example:

```bash
robot --listener MyListener.py path/to/your/tests
```

Multiple listeners can be specified by repeating the `--listener` option.

---

## Listener Pre-run API

The Listener Pre-run API allows you to access and modify test data before the execution starts. This enables dynamic test configuration based on external parameters or other conditions. For detailed information, refer to the [Robot Framework Listener Pre-run API Documentation](https://docs.robotframework.org/docs/extending_robot_framework/listeners_prerun_api/listeners).

---

## Best Practices

- **Keep Processing Minimal:** Listeners should perform lightweight processing to avoid slowing down test execution.
- **Handle Errors Gracefully:** Ensure your listener methods catch exceptions so that they do not disrupt the test run.
- **Separate Concerns:** Use listeners mainly for reporting, logging, or integration tasks—not for complex business logic.

---

## Advanced Topics

- **Multiple Listeners:** When multiple listeners are registered, they are executed in the order specified on the command line.
- **Dynamic Registration:** Listeners can be added dynamically using the pre-run API if your tests require runtime customization.
- **Custom Output:** Listeners can be used to generate custom output formats (e.g., JSON, XML) or integrate with external dashboards and CI/CD tools.
