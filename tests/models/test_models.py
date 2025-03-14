from datetime import datetime, UTC
from app.models.client import Client
from app.models.project import Project
from app.models.activity import Activity


def test_client_model():
    created_at = datetime.now(UTC)
    updated_at = datetime.now(UTC)
    client = Client(
        name="Test Client",
        email="test@example.com",
        created_at=created_at,
        updated_at=updated_at
    )

    assert client.name == "Test Client"
    assert client.email == "test@example.com"
    assert client.projects == []
    assert client.created_at == created_at
    assert client.updated_at == updated_at


def test_project_model():
    created_at = datetime.now(UTC)
    updated_at = datetime.now(UTC)
    client = Client(
        name="Test Client",
        email="test@example.com"
    )

    project = Project(
        name="Test Project",
        description="Test Description",
        status="Open",
        client=client,
        created_at=created_at,
        updated_at=updated_at
    )

    assert project.name == "Test Project"
    assert project.description == "Test Description"
    assert project.status == "Open"
    assert project.client == client
    assert project.activities == []
    assert project.created_at == created_at
    assert project.updated_at == updated_at


def test_activity_model():
    start_time = datetime.now(UTC)
    created_at = datetime.now(UTC)
    project = Project(
        name="Test Project",
        description="Test Description",
        status="Open"
    )

    activity = Activity(
        description="Test Activity",
        project=project,
        start_time=start_time,
        created_at=created_at
    )

    assert activity.description == "Test Activity"
    assert activity.project == project
    assert activity.start_time == start_time
    assert activity.end_time is None
    assert activity.created_at == created_at


def test_client_project_relationship():
    client = Client(
        name="Test Client",
        email="test@example.com"
    )

    project1 = Project(
        name="Project 1",
        description="Description 1",
        status="Open"
    )
    project1.client = client

    project2 = Project(
        name="Project 2",
        description="Description 2",
        status="In Progress"
    )
    project2.client = client

    assert len(client.projects) == 2
    assert project1 in client.projects
    assert project2 in client.projects


def test_project_activity_relationship():
    project = Project(
        name="Test Project",
        description="Test Description",
        status="Open"
    )

    activity1 = Activity(
        description="Activity 1",
        start_time=datetime.now(UTC)
    )
    activity1.project = project

    activity2 = Activity(
        description="Activity 2",
        start_time=datetime.now(UTC)
    )
    activity2.project = project

    assert len(project.activities) == 2
    assert activity1 in project.activities
    assert activity2 in project.activities
