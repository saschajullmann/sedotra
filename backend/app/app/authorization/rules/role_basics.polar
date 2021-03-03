# RBAC BASE POLICY

### Users inherit dataroom roles from their teams
user_in_role(user: User, role, room: Dataroom) if
	team in user.teams and
	role in team.dataroom_roles and
	role.dataroom.id = room.id;

# Get the user's role for a specific Dataroom resource
# Roles are accessed by resource on the user object
user_in_role_for_resource(user: User, role, room: Dataroom) if
    role.user.id = user.id and
    role.dataroom.id = room.id;

# RESOURCE-ROLE RELATIONSHIPS

## These rules allow roles to apply to resources other than those that they are scoped to.
## The most common example of this is nested resources, e.g. Dataroom roles should apply to the Documents
## nested in that dataroom.


### An organization's roles apply to its child datarooms
resource_role_applies_to(room: Dataroom, parent_org) if
    parent_org = room.organization and
    parent_org matches Organization;

### An organization's roles apply to its child teams
resource_role_applies_to(team: Team, parent_org) if
    parent_org = team.organization and
    parent_org matches Organization;

### An organization's roles apply to its child roles
resource_role_applies_to(role: OrganizationRole, parent_org) if
    parent_org = role.organization and
    parent_org matches Organization;

### A dataroom's roles apply to its child roles
resource_role_applies_to(role: DataRoomRole, parent_room) if
    parent_room = role.dataroom and
    parent_room matches Dataroom;

### An organization's roles apply to its child repository's roles
resource_role_applies_to(role: DataRoomRole, parent_org) if
    parent_org = role.dataroom.organization and
    parent_org matches Organization;

### A dataroom's roles apply to its child documents
resource_role_applies_to(doc: Document, parent_room) if
    parent_room = doc.dataroom;


## Role Hierarchies

### Specify repository role order (most senior on left)
dataroom_role_order(["OWNER", "ADMIN", "MEMBER", "GUEST_WRITE", "GUEST_READ"]);

### Specify organization role order (most senior on left)
organization_role_order(["ADMIN", "LEAD", "MEMBER"]);

### Specify team role order (most senior on left)