# validators.py
from typing import Annotated, List
from pydantic import Field

# 🔹 Общие строковые типы
SlugStr = Annotated[str, Field(pattern=r'^[a-z0-9-]{3,50}$', strip_whitespace=True)]
LocaleStr = Annotated[str, Field(pattern=r'^[a-z]{2}(-[A-Z]{2})?$', min_length=2, max_length=10)]
TitleStr = Annotated[str, Field(min_length=3, max_length=200, strip_whitespace=True)]
DescriptionStr = Annotated[str, Field(max_length=1000)]
BodyStr = Annotated[str, Field(min_length=1, max_length=20000)]
ChangelogStr = Annotated[str, Field(max_length=1000)]
TagStr = Annotated[str, Field(min_length=1, max_length=30, strip_whitespace=True)]
LangStr = Annotated[str, Field(min_length=2, max_length=20, strip_whitespace=True)]
CodeStr = Annotated[str, Field(min_length=1, max_length=20000)]

# 🔹 Числовые типы
PositiveInt = Annotated[int, Field(gt=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
VersionInt = Annotated[int, Field(ge=1)]

# 🔹 Списки
TagList = Annotated[List[TagStr], Field(min_length=1, max_length=20)]
OptionsList = Annotated[List[str], Field(min_length=2, max_length=10)]

# 🔹 For auth
PasswordStr = Annotated[str, Field(min_length=8, max_length=128, strip_whitespace=True)]
NameStr = Annotated[str, Field(min_length=3, max_length=50, strip_whitespace=True)]
DescriptionStr_auth = Annotated[str, Field(min_length=3, max_length=255, strip_whitespace=True)]
