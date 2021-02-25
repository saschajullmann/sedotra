from uuid import UUID
from dataclasses import dataclass
from sqlalchemy.orm import Session
from app.models import (
    User,
    Organization,
    Dataroom,
    Document,
)
from sqlalchemy_oso import roles as oso_roles


@dataclass
class Data:
    admin_user_org_1: User
    member_user_org_1: User
    lead_user_org_1: User
    member_user_room_1: User
    guest_read_user_room_1: User
    guest_write_user_room_1: User
    admin_user_room_1: User
    first_org: Organization
    second_org: Organization
    room_1: Dataroom
    room_2: Dataroom
    document_room_1: Document
    document_room_2: Document


def load_role_fixtures(db: Session):
    # Database entities don't get greated with
    # SQLalchemy models directly. This is for testing
    # only.

    admin_user_org_1 = User(
        first_name="Admin",
        last_name="User",
        email="admin@org1.com",
        hashed_password="hash",
    )
    member_user_org_1 = User(
        first_name="First",
        last_name="User",
        email="first@org1.com",
        hashed_password="hash",
    )
    member_user_room_1 = User(
        first_name="Member",
        last_name="User",
        email="member_room1@org1.com",
        hashed_password="hash",
    )
    lead_user_org_1 = User(
        first_name="Second",
        last_name="User",
        email="second@org1.com",
        hashed_password="hash",
    )
    guest_read_user_room_1 = User(
        first_name="Third",
        last_name="User",
        email="guest_read1@room1.com",
        hashed_password="hash",
    )
    guest_write_user_room_1 = User(
        first_name="Third",
        last_name="User",
        email="guest_write1@room1.com",
        hashed_password="hash",
    )
    admin_user_room_1 = User(
        first_name="Fourth",
        last_name="User",
        email="fourth@org2.com",
        hashed_password="hash",
    )
    users = [
        admin_user_org_1,
        member_user_org_1,
        member_user_room_1,
        lead_user_org_1,
        guest_read_user_room_1,
        guest_write_user_room_1,
        admin_user_room_1,
    ]

    db.add_all(users)

    first_org = Organization(name="Org1", description="org1")
    second_org = Organization(name="Org2", description="org2")
    organizations = [first_org, second_org]

    db.add_all(organizations)

    oso_roles.add_user_role(db, admin_user_org_1, first_org, "ADMIN")
    oso_roles.add_user_role(db, member_user_org_1, first_org, "MEMBER")
    oso_roles.add_user_role(db, lead_user_org_1, first_org, "LEAD")

    room_1 = Dataroom(
        name="FirstRoom",
        description="First room",
        creator=lead_user_org_1,
        organization=first_org,
    )

    room_2 = Dataroom(
        name="SecondRoom",
        description="Second room",
        creator=lead_user_org_1,
        organization=first_org,
    )

    document_room_1 = Document(
        name="Test Document",
        description="Test",
        file_name="hallo",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3545"),
        mime_type="text/plain",
        size=50,
        creator=member_user_org_1,
        dataroom=room_1,
    )

    document_room_2 = Document(
        name="Test Document",
        description="Test",
        file_name="second_doc",
        extension="txt",
        md5_sum=UUID("87a6909ab71ec463f013325dbf9f3546"),
        mime_type="text/plain",
        size=50,
        creator=member_user_org_1,
        dataroom=room_2,
    )

    # room1_creator
    oso_roles.add_user_role(db, member_user_org_1, room_1, "OWNER")
    oso_roles.add_user_role(db, lead_user_org_1, room_2, "OWNER")
    oso_roles.add_user_role(db, admin_user_room_1, room_1, "ADMIN")
    oso_roles.add_user_role(db, member_user_room_1, room_1, "MEMBER")
    oso_roles.add_user_role(db, guest_read_user_room_1, room_1, "GUEST_READ")
    oso_roles.add_user_role(db, guest_write_user_room_1, room_1, "GUEST_WRITE")

    rooms = [room_1, room_2]

    documents = [document_room_1, document_room_2]

    db.add_all(rooms)
    db.add_all(documents)

    db.commit()

    for user in users:
        db.refresh(user)

    for org in organizations:
        db.refresh(org)

    for room in rooms:
        db.refresh(room)

    for doc in documents:
        db.refresh(doc)

    return_data = Data(
        admin_user_org_1=admin_user_org_1,
        member_user_org_1=member_user_org_1,
        member_user_room_1=member_user_room_1,
        lead_user_org_1=lead_user_org_1,
        guest_read_user_room_1=guest_read_user_room_1,
        guest_write_user_room_1=guest_write_user_room_1,
        admin_user_room_1=admin_user_room_1,
        first_org=first_org,
        second_org=second_org,
        room_1=room_1,
        room_2=room_2,
        document_room_1=document_room_1,
        document_room_2=document_room_2,
    )
    return return_data
