from datetime import datetime
from patterns.observer.observer import Observer


class NotificationService(Observer):
    """Observer: mencatat semua notifikasi untuk Dashboard Notifikasi."""

    def __init__(self):
        self._notifications = []

    def update(self, event_type, reservation, message):
        self._notifications.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": event_type,
            "reservation_id": reservation.res_id,
            "user_name": reservation.user_name,
            "message": message,
        })

    def get_for(self, user):
        # terbaru di atas; admin melihat semua, pemohon hanya miliknya
        items = list(reversed(self._notifications))
        if user.is_admin():
            return items
        return [n for n in items if n["user_name"] == user.name]