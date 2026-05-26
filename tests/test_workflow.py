from core.workflow import run


def test_coding_workflow():

    result = run(
        "Write a binary search in python"
    )

    assert result["status"] in [
        "completed",
        "failed"
    ]


def test_research_workflow():

    result = run(
        "Research quantum computing"
    )

    assert result["task_type"] == "research"


def test_writer_workflow():

    result = run(
        "Write a README for FastAPI"
    )

    assert result["task_type"] == "writing"


def test_review_workflow():

    result = run(
        "Review this code quality"
    )

    assert result["task_type"] == "review"