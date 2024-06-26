import os
import git

class RepoWrapper:
  remoteDev = 'origin/dev'
  dev = 'dev'

  def __init__(self, url, idx, baseRepoDir, fetchBefore=True) -> None:
    self.url = url
    self.idx = idx
    self.baseRepoDir = baseRepoDir
    self.fetchBefore = fetchBefore

    parts = url.split("/")
    self.name = parts[len(parts)-1].split(".")[0]


  def getDirName(self):
    leading = ''
    if self.idx < 10:
      leading = '0'
    return f'{leading}{self.idx}_{self.name}'

  def init(self):
    repoDirPath = os.path.join(self.baseRepoDir, self.getDirName())

    if not os.path.isdir(repoDirPath):
      self.repo = self.cloneRepo()
    else:
      self.repo = git.Repo(repoDirPath)
      if self.fetchBefore:
        self.repo.remotes.origin.fetch()

  def cloneRepo(self):
    repoDirPath = os.path.join(self.baseRepoDir, self.getDirName())
    #return git.Repo.clone_from(self.url, repoDirPath)
    return git.Repo.clone_from(
      self.url, 
      repoDirPath,
      multi_options=[
        "--filter=blob:none",
        "--no-checkout",
        "--single-branch",
      ],
      branch="dev"
    )
   #git clone --filter=blob:none --no-checkout --single-branch --branch dev ssh://git@git.sfera.inno.local:7999/PPRS/pprs-transactions.git
  
  
  def checkoutDev(self):
    repo = self.repo
    if repo.is_dirty():
      repo.head.reset(index=True, working_tree=True)
    
      repo.git.checkout(self.dev)
      repo.head.reset(index=True, working_tree=True)
      repo.git.pull()

  def getCommits(self):
    repo = self.repo
    #res = repo.git.log(pretty="format:%s")
    #log.info(res)
    commits = repo.iter_commits()

    #return [c.message.rstrip() for c in commits]
    return commits
  