"""
Provides custom exceptions
"""

class QuitError(Exception):
    """Raised when the programme wants to quit the current state."""


class StopError(Exception):
    """Raised when the programme wants to stop."""
