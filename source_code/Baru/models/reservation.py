from patterns.state.reservation_state import PendingState, state_from_name


class Reservation:

  def __init__(self, res_id, user_name, room, date_str, time_str, duration_hours, purpose=""):
    self.res_id = res_id
    self.user_name = user_name
    self.room = room
    self.date_str = date_str
    self.time_str = time_str
    self.duration_hours = duration_hours
    self.purpose = purpose
    self.state = PendingState()

  @property
  def status(self):
    return self.state.name

  @status.setter
  def status(self, value):
    self.state = state_from_name(value)

  @property
  def is_active(self):
    return self.state.blocks_schedule

  @property
  def is_reviewable(self):
    return self.state.reviewable
  
  def approve(self):
    return self.state.approve(self)

  def reject(self):
    return self.state.reject(self)

  def cancel(self):
    return self.state.cancel(self)