"""Exceptions for CEMM."""


class CEMMError(Exception):
    """General CEMM exception."""


class CEMMConnectionError(CEMMError):
    """CEMM connection exception."""
