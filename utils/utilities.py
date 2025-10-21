# time_utils.py

from datetime import datetime

class Utils:
    @staticmethod
    def get_time_period() -> str:
            """Returns the time of day: 'morning', 'afternoon', or 'evening'"""
            now = datetime.now()
            hour = now.hour

            if 5 <= hour < 12:
                return "morning"
            elif 12 <= hour < 18:
                return "afternoon"
            else:
                return "evening"