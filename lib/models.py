class Commit:
  def __init__(self, sha, message, date) -> None:
    self.sha = sha
    self.message = message
    self.date = date
  
  def __iter__(self):
    return iter([self.sha, self.message, self.date])

class Issue:
  def __init__(self, id, title, body, state, created_at, closed_at, pull_request) -> None:
    self.id = id
    self.title = title
    self.body = body
    self.state = state
    self.created_at = created_at
    self.closed_at = closed_at

    if pull_request is None:
      self.is_pull_request = False
      self.merged_at = None
    else:
      self.is_pull_request = True
      self.merged_at = pull_request['merged_at']

  def __iter__(self):
    return iter([self.id, self.title, self.body, self.state, self.created_at, self.closed_at, self.is_pull_request, self.merged_at])
  
class PullRequest:
  def __init__(self, merged_at) -> None:
    self.merged_at = merged_at
  
  def __iter__(self):
    return iter([self.merged_at])

class Tag:
  def __init__(self, name, sha) -> None:
    self.name = name
    self.sha = sha

  def __iter__(self):
    return iter([self.name, self.sha])
