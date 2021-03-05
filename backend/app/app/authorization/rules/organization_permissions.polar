### Permissions to all org roles
role_allow(_role: OrganizationRole, "READ", _org: Organization);
role_allow(_role: OrganizationRole, "LIST_TEAMS", _org: Organization);
role_allow(_role: OrganizationRole, "LIST_ROOMS", _org: Organization);

### Admin permissions
role_allow(_role: OrganizationRole{name: "ADMIN"}, "LIST_ROLES", _org: Organization);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "UPDATE", _org: Organization);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "DELETE", _team: Team);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "CREATE", _role_resource: OrganizationRole);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "READ", _role_resource: OrganizationRole);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "UPDATE", _role_resource: OrganizationRole);
role_allow(_role: OrganizationRole{name: "ADMIN"}, "DELETE", _role_resource: OrganizationRole);


### Lead permissions
role_allow(_role: OrganizationRole{name: "LEAD"}, "CREATE", _team: Team);
### Member permissions
role_allow(_role: OrganizationRole{name: "MEMBER"}, "CREATE", _room: Dataroom);
role_allow(_role: OrganizationRole{name: "MEMBER"}, "READ", _room: Dataroom);
role_allow(_role: OrganizationRole{name: "MEMBER"}, "READ", _team: Team);