import flet as ft
from services.room_service import RoomService
from services.user_service import UserService
from services.reservation_service import ReservationService
from services.notification_service import NotificationService
from views.app_shell import AppShell

def main(page: ft.Page):
    room_service = RoomService()
    user_service = UserService()
    reservation_service = ReservationService(
        room_service=room_service, user_service=user_service
    )

    notification_service = NotificationService()
    reservation_service.attach(notification_service)

    shell = AppShell(page, room_service, reservation_service, user_service, notification_service)
    reservation_service.attach(shell)

if __name__ == "__main__":
    ft.run(main)