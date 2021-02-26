from typing import List
from uuid import UUID
from oso import Oso
from app.models import (
    Team,
    OrganizationRole,
    Dataroom,
)
from sqlalchemy.orm import Session
from app.models.document import Document
from sqlalchemy_oso import roles as oso_roles

from tests.fixtures.role_data import Data


def test_org_roles(db: Session, data: Data, oso: Oso):
    # Any type of org role can read the specific org but not another org
    assert oso.is_allowed(data.member_user_org_1, "READ", data.first_org) is True
    assert oso.is_allowed(data.admin_user_org_1, "READ", data.first_org) is True
    assert oso.is_allowed(data.lead_user_org_1, "READ", data.first_org) is True

    assert oso.is_allowed(data.lead_user_org_1, "READ", data.second_org) is False
    assert oso.is_allowed(data.member_user_org_1, "READ", data.second_org) is False
    assert oso.is_allowed(data.admin_user_org_1, "READ", data.second_org) is False

    # Any type of org role can list all the teams in the specific org
    assert oso.is_allowed(data.member_user_org_1, "LIST_TEAMS", data.first_org) is True
    assert oso.is_allowed(data.admin_user_org_1, "LIST_TEAMS", data.first_org) is True
    assert oso.is_allowed(data.lead_user_org_1, "LIST_TEAMS", data.first_org) is True

    assert oso.is_allowed(data.lead_user_org_1, "LIST_TEAMS", data.second_org) is False
    assert (
        oso.is_allowed(data.member_user_org_1, "LIST_TEAMS", data.second_org) is False
    )
    assert oso.is_allowed(data.admin_user_org_1, "LIST_TEAMS", data.second_org) is False

    # Only admin user can edit the org
    assert oso.is_allowed(data.admin_user_org_1, "UPDATE", data.first_org) is True
    assert oso.is_allowed(data.member_user_org_1, "UPDATE", data.first_org) is False
    assert oso.is_allowed(data.lead_user_org_1, "UPDATE", data.first_org) is False

    # Only admin user can list org roles
    assert oso.is_allowed(data.admin_user_org_1, "LIST_ROLES", data.first_org) is True
    assert oso.is_allowed(data.member_user_org_1, "LIST_ROLES", data.first_org) is False
    assert oso.is_allowed(data.lead_user_org_1, "LIST_ROLES", data.first_org) is False

    # Only admin user can add interact with org roles
    new_role_insert = OrganizationRole(
        name="MEMBER", organization=data.first_org, user=data.guest_read_user_room_1
    )  # type: ignore
    assert oso.is_allowed(data.admin_user_org_1, "CREATE", new_role_insert) is True
    assert oso.is_allowed(data.admin_user_org_1, "READ", new_role_insert) is True
    assert oso.is_allowed(data.admin_user_org_1, "UPDATE", new_role_insert) is True
    assert oso.is_allowed(data.admin_user_org_1, "DELETE", new_role_insert) is True
    assert oso.is_allowed(data.member_user_org_1, "CREATE", new_role_insert) is False
    assert oso.is_allowed(data.member_user_org_1, "READ", new_role_insert) is False
    assert oso.is_allowed(data.member_user_org_1, "UPDATE", new_role_insert) is False
    assert oso.is_allowed(data.member_user_org_1, "DELETE", new_role_insert) is False
    assert oso.is_allowed(data.lead_user_org_1, "CREATE", new_role_insert) is False
    assert oso.is_allowed(data.lead_user_org_1, "READ", new_role_insert) is False
    assert oso.is_allowed(data.lead_user_org_1, "UPDATE", new_role_insert) is False
    assert oso.is_allowed(data.lead_user_org_1, "DELETE", new_role_insert) is False

    # Only admins and leads can create teams not member
    new_team_resource = Team(
        "TestTeam",
        "This is a test",
        True,
        creator=data.admin_user_org_1,
        organization=data.first_org,
    )
    assert oso.is_allowed(data.admin_user_org_1, "CREATE", new_team_resource) is True
    assert oso.is_allowed(data.lead_user_org_1, "CREATE", new_team_resource) is True
    assert oso.is_allowed(data.member_user_org_1, "CREATE", new_team_resource) is False

    # Only admins can delete teams not member and lead
    assert oso.is_allowed(data.admin_user_org_1, "DELETE", new_team_resource) is True
    assert oso.is_allowed(data.lead_user_org_1, "DELETE", new_team_resource) is False
    assert oso.is_allowed(data.member_user_org_1, "DELETE", new_team_resource) is False

    # Any role in the org can read the team
    assert oso.is_allowed(data.admin_user_org_1, "READ", new_team_resource) is True
    assert oso.is_allowed(data.lead_user_org_1, "READ", new_team_resource) is True
    assert oso.is_allowed(data.member_user_org_1, "READ", new_team_resource) is True

    # Anyone in the org can create and read datarooms
    new_dataroom_resource = Dataroom(
        name="MyRoom",
        description="New Room",
        creator=data.admin_user_org_1,
        organization=data.first_org,
    )
    assert (
        oso.is_allowed(data.admin_user_org_1, "CREATE", new_dataroom_resource) is True
    )
    assert oso.is_allowed(data.lead_user_org_1, "CREATE", new_dataroom_resource) is True
    assert (
        oso.is_allowed(data.member_user_org_1, "CREATE", new_dataroom_resource) is True
    )
    assert oso.is_allowed(data.admin_user_org_1, "READ", new_dataroom_resource) is True
    assert oso.is_allowed(data.lead_user_org_1, "READ", new_dataroom_resource) is True
    assert oso.is_allowed(data.member_user_org_1, "READ", new_dataroom_resource) is True


def test_dataroom_roles(db: Session, data: Data, oso: Oso):
    # Guest can access the documents for the room in which he is guest
    assert oso.is_allowed(data.guest_read_user_room_1, "READ", data.room_1) is True
    assert (
        oso.is_allowed(data.guest_read_user_room_1, "LIST_DOCUMENTS", data.room_1)
        is True
    )
    assert (
        oso.is_allowed(data.guest_read_user_room_1, "READ", data.document_room_1)
        is True
    )

    # Guest cannot see other datarooms
    assert (
        oso.is_allowed(data.guest_read_user_room_1, "LIST_ROOMS", data.first_org)
        is False
    )
    assert oso.is_allowed(data.guest_read_user_room_1, "READ", data.room_2) is False
    assert (
        oso.is_allowed(data.guest_read_user_room_1, "READ", data.document_room_2)
        is False
    )

    new_document_guest_1 = Document(
        name="Test Document",
        description="Test",
        file_name="hallo",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3541"),
        mime_type="text/plain",
        size=50,
        creator=data.guest_read_user_room_1,
        dataroom=data.room_1,
    )

    new_document_guest_2 = Document(
        name="New Doc Guest 2",
        description="Test",
        file_name="new_doc_guest_2",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3541"),
        mime_type="text/plain",
        size=50,
        creator=data.guest_write_user_room_1,
        dataroom=data.room_1,
    )

    # Only guest with write access can create a new document
    assert (
        oso.is_allowed(data.guest_write_user_room_1, "CREATE", new_document_guest_2)
        is True
    )
    assert (
        oso.is_allowed(data.guest_read_user_room_1, "CREATE", new_document_guest_1)
        is False
    )

    # add the second new document to db so that we can test edits
    db.add(new_document_guest_2)
    db.commit()
    db.refresh(new_document_guest_2)

    assert (
        oso.is_allowed(data.guest_write_user_room_1, "UPDATE", new_document_guest_2)
        is True
    )
    assert (
        oso.is_allowed(data.guest_write_user_room_1, "DELETE", new_document_guest_2)
        is True
    )
    assert (
        oso.is_allowed(data.guest_write_user_room_1, "UPDATE", data.document_room_1)
        is False
    )
    assert (
        oso.is_allowed(data.guest_write_user_room_1, "DELETE", data.document_room_1)
        is False
    )
    assert (
        oso.is_allowed(data.admin_user_room_1, "UPDATE", data.document_room_1) is True
    )
    assert (
        oso.is_allowed(data.admin_user_room_1, "DELETE", data.document_room_1) is True
    )

    # Only OWNERS can delete a dataroom
    assert oso.is_allowed(data.member_user_org_1, "DELETE", data.room_1) is True
    assert oso.is_allowed(data.guest_read_user_room_1, "DELETE", data.room_1) is False
    assert oso.is_allowed(data.guest_write_user_room_1, "DELETE", data.room_1) is False

    # Admin are allowed to invite_guests
    assert oso.is_allowed(data.admin_user_room_1, "INVITE_GUESTS", data.room_1) is True
    assert oso.is_allowed(data.admin_user_room_1, "INVITE_GUESTS", data.room_2) is False

    new_document_member_1 = Document(
        name="New Doc Member 1",
        description="Test",
        file_name="new_doc_member_1",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3543"),
        mime_type="text/plain",
        size=50,
        creator=data.member_user_room_1,
        dataroom=data.room_1,
    )

    # Members can create documents and edit and delete their own
    assert (
        oso.is_allowed(data.member_user_room_1, "CREATE", new_document_member_1) is True
    )

    db.add(new_document_member_1)
    db.commit()
    db.refresh(new_document_member_1)

    assert (
        oso.is_allowed(data.member_user_room_1, "UPDATE", new_document_member_1) is True
    )
    assert (
        oso.is_allowed(data.member_user_room_1, "DELETE", new_document_member_1) is True
    )

    assert (
        oso.is_allowed(data.member_user_room_1, "UPDATE", new_document_guest_2) is False
    )
    assert (
        oso.is_allowed(data.member_user_room_1, "DELETE", new_document_guest_2) is False
    )


def test_team_dataroom_roles(db: Session, data: Data, oso: Oso):
    # make sure that a user that does not have direct
    # room roles can still manage room because of a team
    # role
    user_roles_in_room_1: List = oso_roles.get_user_roles(
        db, data.member_team_1, Dataroom, data.room_1.id
    )

    # user does not have direct access to the room
    count_of_roles = len(user_roles_in_room_1)
    assert count_of_roles == 0

    # but still gets it via his team role (which is a members role)
    assert oso.is_allowed(data.member_team_1, "READ", data.room_1) is True
    assert oso.is_allowed(data.member_team_1, "LIST_DOCUMENTS", data.room_1) is True
    assert oso.is_allowed(data.member_team_1, "DELETE", data.room_1) is False
    assert oso.is_allowed(data.member_team_1, "UPDATE", data.room_1) is False
    assert oso.is_allowed(data.member_team_1, "INVITE_GUESTS", data.room_1) is False

    # does not have access to other rooms
    assert oso.is_allowed(data.member_team_1, "READ", data.room_2) is False
    assert oso.is_allowed(data.member_team_1, "LIST_DOCUMENTS", data.room_2) is False

    # is allowed to create his own documents in a room
    new_document_team_member_1 = Document(
        name="New Doc Team Member 1",
        description="Test",
        file_name="new_doc_team_member_1",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3543"),
        mime_type="text/plain",
        size=50,
        creator=data.member_team_1,
        dataroom=data.room_1,
    )

    assert (
        oso.is_allowed(data.member_team_1, "CREATE", new_document_team_member_1) is True
    )
