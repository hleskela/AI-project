Git is a version control system that makes it easier to share bigger projects between people. Similar version control systems would be mercurial or rcs (but rcs sucks).
Github is a page that hosts these repos, so that we don't have to keep them on some other server (like a LAMP server running git on your RaspberryPI at home ;) )




git clone <http address> - fetch a repository from the address, initiate a git repository (repo) with this on your computer (in the directory where you issue the command).
git status - show the status of your local repo. This includes (but doesn't exclude other info) if you have files that are not a part of git, if some files need to be added before you can commit them, and if you have commits that you can push to the main repo.
git pull - to get changes that has been uploaded to the git repo
git push - to submit changes to the git repo
git add - add a new file that git will keep track of, or to add a changed file to the "to be commited" stack
git commit - create a commit of all the changes that you have added (i.e. changes in files that has been "git add":ed)
git branch - view your branches and on what branch you are
git branch <branch-name> - creates a new branch so that you don't work on master, the main branch.
git checkout <branch-name> - switch to the branch stated, i.e. start working on a new branch.




Issuing "man git" in the terminal will give you all the stuff you could possibly want to know about git. 
If you want to know something about git, either ask Google, or Sarah and/or Hannes. If you don't know what you want to ask, ask Sarah... or Hannes. But not Google.