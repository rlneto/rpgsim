"""
UI Exceptions
Custom exceptions for UI module
"""


class UIException(Exception):
    """Base UI exception"""
    pass


class UIStateError(UIException):
    """UI state related errors"""
    pass


class ScreenNotFoundError(UIStateError):
    """Screen not found error"""
    pass


class InvalidNavigationError(UIStateError):
    """Invalid navigation error"""
    pass


class AnimationError(UIException):
    """Animation related errors"""
    pass


class RenderError(UIException):
    """Rendering related errors"""
    pass


class InputError(UIException):
    """Input handling errors"""
    pass


class ThemeError(UIException):
    """Theme related errors"""
    pass


class ResourceError(UIException):
    """Resource loading errors"""
    pass


class ConfigurationError(UIException):
    """Configuration related errors"""
    pass


class WidgetError(UIException):
    """Widget related errors"""
    pass


class LayoutError(UIException):
    """Layout related errors"""
    pass