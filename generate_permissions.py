from auth.models import Permission

def generate_permissions(session, models):
    permissions = []
    actions = ["CREATE", "READ", "UPDATE", "DELETE"]

    for model in models:
        for action in actions:
            permissions.append(
                {
                    "name": f"{action}_{model.__name__.upper()}",
                    "description": f"Allows the user to {action.lower()} {model.__name__.lower()} recprds",
                }
            )
    session.execute(Permission.__table__.insert(), permissions)
    session.commit()
    