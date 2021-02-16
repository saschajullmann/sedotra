# oso policy

# ROLE-PERMISSION RELATIONSHIPS

## Organization Permissions

### All organization roles let users read the organization
role_allow(_role: TeamRole, "READ", _org: Team);

### The member role can list datarooms in the team
role_allow(_role: TeamRole{name: "MEMBER"}, "LIST_DATAROOMS", _org: Team);

### The owner role can assign roles within the org
role_allow(_role: TeamRole{name: "OWNER"}, "CREATE_ROLE", _org: Team);
role_allow(_role: TeamRole{name: "OWNER"}, "READ_ROOM", _resource: Dataroom);

#resource_role_applies_to(room: Dataroom, parent_org) if
#    parent_org := room.team and
#    parent_org matches Team;