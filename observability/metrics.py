from prometheus_client import Counter

workflow_success = Counter(
    "workflow_success_total",
    "Successful workflows"
)

workflow_failure = Counter(
    "workflow_failure_total",
    "Failed workflows"
)

workflow_retry = Counter(
    "workflow_retry_total",
    "Workflow retries"
)