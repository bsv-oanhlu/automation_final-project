"""Shared locator fragments — prefer role/label/placeholder in page objects first."""


class CommonLocators:
    """Structural scopes (#id) when role/label cannot disambiguate duplicate UI."""

    TOAST_CONTAINER = "#toast_container"
    TICKET_TABLE_BODY = "#ticket_tbody"
    NOTIFICATION_TABLE_BODY = "#notification_tbody"
    NAV_TABS = "#nav_tabs"
    PANEL_TICKETS = "#panel_tickets"
    PANEL_NOTIFICATIONS = "#panel_notifications"


class DatePickerLocators:
    """Reserved for shared date-picker patterns (not used on this exercise site)."""

    pass
