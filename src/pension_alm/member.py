from dataclasses import dataclass
from enum import Enum


class MemberStatus(Enum):
    """Employment status of a pension scheme member."""

    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    DEFERRED = "DEFERRED"


class Sex(Enum):
    """Biological sex used for mortality modelling."""

    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass(frozen=True, slots=True)
class Member:
    """Pension scheme member.

    This entity stores member-level information required by the ALM model.

    Notes
    -----
    The class intentionally stores only member facts.

    Financial calculations such as

    - mortality projection,
    - pension projection,
    - liability valuation,
    - funding ratio,

    are implemented by other components of the framework.
    """

    member_id: str

    age: int

    sex: Sex

    status: MemberStatus

    annual_pension: float

    retirement_age: int

    def __post_init__(self) -> None:

        if not self.member_id:
            raise ValueError("member_id must not be empty")

        if self.age < 0:
            raise ValueError("age must be non-negative")

        if self.annual_pension < 0:
            raise ValueError("annual_pension must be non-negative")

        if self.retirement_age <= 0:
            raise ValueError("retirement_age must be positive")

        if self.retirement_age < self.age and self.status == MemberStatus.ACTIVE:
            raise ValueError(
                "Active member cannot be older than retirement age."
            )

    @property
    def is_active(self) -> bool:
        """Return True if the member is active."""
        return self.status == MemberStatus.ACTIVE

    @property
    def is_retired(self) -> bool:
        """Return True if the member is retired."""
        return self.status == MemberStatus.RETIRED

    @property
    def is_deferred(self) -> bool:
        """Return True if the member has a deferred pension."""
        return self.status == MemberStatus.DEFERRED

    @property
    def years_to_retirement(self) -> int:
        """Return the remaining years until retirement."""
        return max(0, self.retirement_age - self.age)