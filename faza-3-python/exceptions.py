class PhaseOneError(Exception):
    """Base class for exceptions in phase one."""


class UTXONotFoundError(PhaseOneError):
    """Exception raised when a UTXO is not found."""


class DoubleSpendingError(PhaseOneError):
    """Exception raised when double spending is detected."""


class NegativeValueError(PhaseOneError):
    """Exception raised when a negative value is encountered."""


class OverSpendingError(PhaseOneError):
    """Exception raised when over spending is detected."""


class VerificationError(PhaseOneError):
    """Exception raised when verification fails."""
