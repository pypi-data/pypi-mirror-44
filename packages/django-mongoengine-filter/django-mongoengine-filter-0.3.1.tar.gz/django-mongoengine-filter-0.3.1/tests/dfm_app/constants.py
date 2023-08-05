__all__ = (
    "PROFILE_TYPE_FREE",
    "PROFILE_TYPE_MEMBER",
    "PROFILE_TYPES",
    "PROFILE_TYPES_CHOICES",
    "GENDER_MALE",
    "GENDER_FEMALE",
    "GENDERS",
)

PROFILE_TYPE_FREE = "free"
PROFILE_TYPE_MEMBER = "member"
PROFILE_TYPES = (PROFILE_TYPE_FREE, PROFILE_TYPE_MEMBER)
PROFILE_TYPES_CHOICES = (
    (PROFILE_TYPE_FREE, "Free"),
    (PROFILE_TYPE_MEMBER, "Member"),
)

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDERS = (GENDER_MALE, GENDER_FEMALE)
