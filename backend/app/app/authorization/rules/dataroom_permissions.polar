### Read role can read the repository
role_allow(_role: DataRoomRole{name: "OWNER"}, "DELETE", _room: Dataroom);

### ADMIN ROLES
role_allow(_role: DataRoomRole{name: "ADMIN"}, "UPDATE", _room: Dataroom);
role_allow(_role: DataRoomRole{name: "ADMIN"}, "INVITE_GUESTS", _room: Dataroom);
role_allow(_role: DataRoomRole{name: "ADMIN"}, "UPDATE", _doc: Document);
role_allow(_role: DataRoomRole{name: "ADMIN"}, "DELETE", _doc: Document);

### MEMBER ROLES
role_allow(_role: DataRoomRole{name: "MEMBER"}, "READ", _room: Dataroom);

### GUEST ROLES
role_allow(_role: DataRoomRole{name: "GUEST_READ"}, "READ", _room: Dataroom);
role_allow(_role: DataRoomRole{name: "GUEST_READ"}, "READ", _doc: Document);
role_allow(_role: DataRoomRole{name: "GUEST_READ"}, "LIST_DOCUMENTS", _room: Dataroom);
role_allow(_role: DataRoomRole{name: "GUEST_WRITE"}, "CREATE", _doc: Document);


### Rules for all roles
role_allow(_role: DataRoomRole, "UPDATE", _doc: Document) if
    doc_owner(_role.user, _doc);
role_allow(_role: DataRoomRole, "DELETE", _doc: Document) if
    doc_owner(_role.user, _doc);

doc_owner(_actor: User, _doc: Document) if
    _actor.id = _doc.created_by;
