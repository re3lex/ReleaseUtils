import colorlog
import os
import git

fmt = '%(log_color)s%(asctime)s [%(levelname)-8s] %(message)s (%(filename)s:%(lineno)d)'

colorlog.basicConfig(format=fmt, level=colorlog.INFO)
log = colorlog.getLogger()

from src.FileGenerator import FileGenerator


outputDir = 'out'
tasksByReposFile = f'{outputDir}/tasksByRepos.txt'
reposByTasksFile = f'{outputDir}/reposByTasks.txt'

if __name__ == '__main__':
  if not os.path.exists(outputDir):
      os.makedirs(outputDir)  

  gen = FileGenerator(tasksByReposFile=tasksByReposFile, reposByTasksFile=reposByTasksFile)
  gen.generate()
  
  print(' ')
  print(' ')

  log.info(f'Check tasks by repos list in file {tasksByReposFile}')
  log.info(f'Check repos by tasks list in file {reposByTasksFile}')