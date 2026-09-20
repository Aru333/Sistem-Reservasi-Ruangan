PEMOHON = "PEMOHON"
ADMIN = "ADMIN"


class User:

  def __init__(self, name, role):
    self.name = name
    self.role = role

  def is_admin(self):
    return self.role == ADMIN