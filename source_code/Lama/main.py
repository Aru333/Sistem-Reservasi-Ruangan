import flet as ft
from services.room_service import RoomService
from services.reservation_service import ReservationService
from views.main_view import ReservationAppView

def main(page: ft.Page):
    #inisialisasi RoomService
    room_service = RoomService()
    # masukkan room_service ke ReservationService
    reservation_service = ReservationService(room_service=room_service)
    
    # Jalankan Tampilan
    ReservationAppView(page, room_service, reservation_service)

if __name__ == "__main__":
    ft.run(main)