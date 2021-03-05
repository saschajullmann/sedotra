import uuid
from fastapi.testclient import TestClient
from app.core.config import settings
from tests.fixtures.role_data import Data
from tests.utils.auth_header import create_access_header


def test_get_rooms_in_org(
    client: TestClient,
    data: Data,
) -> None:
    """
    This test is responsible for checking whether certain kinds of
    users can access the the endpoint which lets one get a list of
    all the datarooms in a given org.
    """

    # Make sure a user who is a member of the org can list rooms
    auth_header = create_access_header(data.member_user_org_1)

    response = client.get(
        f"{settings.API_V1_STR}/orgs/{data.first_org.id}/datarooms",
        headers=auth_header,
    )

    assert response.status_code == 200

    # Make sure the same user cannot access the list rooms endpoint
    # for a random org.

    rand_uuid = uuid.uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/orgs/{rand_uuid}/datarooms",
        headers=auth_header,
    )

    assert response.status_code == 404

    # Make sure a guest user with only access to a specific room cannot
    # access the list rooms endpoint for the entire org
    auth_header = create_access_header(data.guest_read_user_room_1)

    response = client.get(
        f"{settings.API_V1_STR}/orgs/{data.first_org.id}/datarooms",
        headers=auth_header,
    )

    assert response.status_code == 400
