# permissions.py

ROLE_PERMISSIONS = {
    "admin": ["*"],  # полный доступ

    "instructor": [
        "content:create", "content:update", "content:view",
        "lesson:create", "lesson:update", "lesson:view",
        "quiz:create", "quiz:update", "quiz:view",
        "example:create", "example:update", "example:view"
    ],

    "reviewer": [
        "content:view", "content:approve",
        "quiz:view", "quiz:approve",
        "lesson:view"
    ],

    "learner": [
        "lesson:view",
        "quiz:view", "quiz:take",
        "example:view",
        "content:view"
    ],

    "collaborator": [
        "content:suggest", "content:edit",
        "lesson:suggest", "lesson:edit",
        "quiz:suggest", "quiz:edit"
    ],
}
