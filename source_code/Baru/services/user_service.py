from models.user import User, PEMOHON, ADMIN


class UserService:

  def __init__(self):
    self.users = [
        User("Muhammad Arden Abdalla", PEMOHON),
        User("Muhammad Hibat", PEMOHON),
        User("Muhammad Arfan", PEMOHON),
        User("Farizi", PEMOHON),
        User("Admin Ruangan", ADMIN),
    ]

  def get_all_users(self):
    return self.users

  def find_by_name(self, name):
    return next((u for u in self.users if u.name == name), None)