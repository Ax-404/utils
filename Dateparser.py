from datetime import datetime, time
from typing import Union, Optional
import pytz

#from previous project
class DateUtils:
    """Utility class for date handling and standardization
    functions:
        parse_datetime: Parse a datetime string into a datetime object
        parse_date: Parse a date string into a datetime object
        parse_time: Parse a time string into a time object
        format_datetime: Format a datetime object into a standardized string
        format_date: Format a datetime object or string into a date string
        format_time: Format a datetime object or string into a time string
    """
    
    # Standard date formats
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    
    # Default timezone
    DEFAULT_TIMEZONE = "Europe/Paris"
    
    @classmethod
    def parse_datetime(cls, date_str: str, timezone: Optional[str] = None) -> datetime:
        """
        Parse a datetime string into a datetime object.
        Handles both ISO format and custom formats.
        
        Args:
            date_str: The datetime string to parse
            timezone: Optional timezone string (defaults to DEFAULT_TIMEZONE)
            
        Returns:
            datetime object with timezone information
        """
        try:
            # Try ISO format first
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            try:
                # Try custom format
                dt = datetime.strptime(date_str, cls.DATETIME_FORMAT)
            except ValueError:
                raise ValueError(f"Invalid datetime format: {date_str}")
        
        # Add timezone if not present
        if dt.tzinfo is None:
            tz = pytz.timezone(timezone or cls.DEFAULT_TIMEZONE)
            dt = tz.localize(dt)
            
        return dt
    
    @classmethod
    def parse_date(cls, date_str: str) -> datetime:
        """
        Parse a date string into a datetime object.
        
        Args:
            date_str: The date string to parse (YYYY-MM-DD)
            
        Returns:
            datetime object at midnight
        """
        try:
            return datetime.strptime(date_str, cls.DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected format: {cls.DATE_FORMAT}")
    
    @classmethod
    def parse_time(cls, time_str: str) -> time:
        """
        Parse a time string into a time object.
        
        Args:
            time_str: The time string to parse (HH:MM)
            
        Returns:
            time object
        """
        try:
            return datetime.strptime(time_str, cls.TIME_FORMAT).time()
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}. Expected format: {cls.TIME_FORMAT}")
    
    @classmethod
    def format_datetime(cls, dt: datetime) -> str:
        """
        Format a datetime object into a standardized string.
        
        Args:
            dt: The datetime object to format
            
        Returns:
            Formatted datetime string
        """
        if dt.tzinfo is None:
            tz = pytz.timezone(cls.DEFAULT_TIMEZONE)
            dt = tz.localize(dt)
        return dt.isoformat()
    
    @classmethod
    def format_date(cls, dt: Union[datetime, str]) -> str:
        """
        Format a datetime object or string into a date string.
        
        Args:
            dt: The datetime object or string to format
            
        Returns:
            Formatted date string (YYYY-MM-DD)
        """
        if isinstance(dt, str):
            dt = cls.parse_datetime(dt)
        return dt.strftime(cls.DATE_FORMAT)
    
    @classmethod
    def format_time(cls, dt: Union[datetime, str]) -> str:
        """
        Format a datetime object or string into a time string.
        
        Args:
            dt: The datetime object or string to format
            
        Returns:
            Formatted time string (HH:MM)
        """
        if isinstance(dt, str):
            dt = cls.parse_datetime(dt)
        return dt.strftime(cls.TIME_FORMAT) 