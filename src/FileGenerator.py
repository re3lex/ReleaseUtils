import colorlog
import os
import git

fmt = '%(log_color)s%(asctime)s [%(levelname)-8s] %(message)s (%(filename)s:%(lineno)d)'

colorlog.basicConfig(format=fmt, level=colorlog.INFO)
log = colorlog.getLogger()

from src.RepoWrapper import RepoWrapper


class FileGenerator:
  tasksFile = 'tasks.txt'
  reposFile = 'repos.txt'
  baseRepoDir = "repos"

  def __init__(self, tasksByReposFile, reposByTasksFile) -> None:
    self.tasksByReposFile = tasksByReposFile
    self.reposByTasksFile = reposByTasksFile
    self.loadReposUrls()
    self.loadTasksFile()

  def loadTasksFile(self):
    self.tasksInRelease = []
    with open(self.tasksFile) as file:
        self.tasksInRelease = [line.lstrip().rstrip() for line in file]

  def loadReposUrls(self):
    self.repoUrls = []
    with open(self.reposFile) as file:
      for line in file:
        s = line.lstrip().rstrip()
        if s.startswith("#") == False:
          self.repoUrls.append(s)


  def writeMapToFile(self, map, fileName):
    with open(fileName, 'w') as the_file:
      for level1 in map:
        the_file.write(f'{level1}\n')
        for level2 in map[level1]:
            the_file.write(f'\t\t{level2}\n')
        
        the_file.write('\n\n')

  def createFileByRepos(self, reposWithTasks):
    self.writeMapToFile(reposWithTasks, self.tasksByReposFile)
    
        
  def createFileByTask(self, reposWithTasks):
    taskMap = {}
    for repo in reposWithTasks:
      for task in reposWithTasks[repo]:
        repos = taskMap.get(task)
        if repos is None:
          repos = []
          taskMap[task] = repos
        repos.append(repo)
    self.writeMapToFile(taskMap, self.reposByTasksFile)
  
  def generate(self):
    reposWithTasks = {}

    if not os.path.isdir(self.baseRepoDir):
      os.mkdir(self.baseRepoDir)

    for idx, repoUrl in enumerate(self.repoUrls):
      print('')
      log.info(f'{idx} Handling repo {repoUrl}')
      gitWrapper = RepoWrapper(repoUrl, idx, self.baseRepoDir)
      try:
        gitWrapper.init()
        #gitWrapper.checkoutDev()
        commits = gitWrapper.getCommits()

        tasksInRepo = []

        for cmt in commits:
          msg = cmt.message.rstrip()
          if msg in self.tasksInRelease:
            tasksInRepo.append(msg)
        
        if len(tasksInRepo) > 0:
          reposWithTasks[gitWrapper.name] = tasksInRepo
      except git.GitCommandError as e:
        log.error(e.stdout or e.stderr)
      except:
          log.exception('')


    self.createFileByRepos(reposWithTasks=reposWithTasks)
    self.createFileByTask(reposWithTasks=reposWithTasks)
    
  
