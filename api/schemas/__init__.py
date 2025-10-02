from .category import CategorySchema, CategoryWithRelationsSchema
from .content import ContentSchema
from .lesson import LessonSchema
from .quiz import QuizSchema
from .example import ExampleSchema
from .content_version import ContentVersionSchema

# 🔹 rebuild всех forward references
CategoryWithRelationsSchema.model_rebuild()
ContentSchema.model_rebuild()
LessonSchema.model_rebuild()
QuizSchema.model_rebuild()
