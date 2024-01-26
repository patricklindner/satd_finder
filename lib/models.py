class Commit:
  def __init__(self, sha, message, date) -> None:
    self.sha = sha
    self.message = message
    self.date = date
  
  def __iter__(self):
    return iter([self.sha, self.message, self.date])

class Issue:
  def __init__(self, id, title, body, state, created_at, closed_at) -> None:
    self.id = id
    self.title = title
    self.body = body
    self.state = state
    self.created_at = created_at
    self.closed_at = closed_at

  def __iter__(self):
    return iter([self.id, self.title, self.body, self.state, self.created_at, self.closed_at])

class Tag:
  def __init__(self, name, sha) -> None:
    self.name = name
    self.sha = sha

  def __iter__(self):
    return iter([self.name, self.sha])
