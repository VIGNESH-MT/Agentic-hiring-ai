class HumanOverrideAgent:
    """
    Enforces governance rules for human overrides.
    """

    ALLOWED_DECISIONS = {"HIRE", "REJECT", "HOLD"}

    def validate_override(
        self,
        *,
        decision: str,
        reason: str,
        reviewer_id: str,
    ) -> None:
        if decision not in self.ALLOWED_DECISIONS:
            raise ValueError("Invalid override decision.")

        if not reason or len(reason.strip()) < 10:
            raise ValueError("Override reason must be at least 10 characters.")

        if not reviewer_id:
            raise ValueError("Reviewer ID is required for governance.")
