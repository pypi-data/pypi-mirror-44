# lethe README

```lethe``` is a Python module for git-based snapshotting.

```lethe``` is intended as a mechanism for creating commits outside 
the standard git branching/tagging workflows. It is meant to enable
additional use-cases without disrupting the standard workflows.
Use cases include:

- Short-lived:
    - On-disk **undo log**
    - **Syncing work-in-progress** between computers before it's ready 
- Long-lived:
    - **lab notebook**: Recording the code / configuration state that resulted in a given output
    - **incremental backup**: Space-efficient time-based backups of a codebase 


## Usage

### Creating a commit from the command line 
```bash
$ cd path/to/repo
$ lethe
122d058e375274a186c407f28602c3b14a2cab95
```
This effectively snapshots the current state of the repository (as would be seen by
```git add --all```) and creates a new commit (```122d058e375274a186c407f28602c3b14a2cab95```)
which points to it. The current branch and index are not changed.

### Flags:
- ```-p my_parent_ref``` is used to provide "parent" refs which become the parents of the created commit.
If a parent ref is a symbolic ref, *both* the provided ref and the ref it points to are used as parents.
If not present, defaults to ```-p HEAD```.
- ```-t ref/lethe/my_target_ref``` is used to provide "target" refs which will be created/updated
to point to the created commit.
If not present, defaults to adding an entry of the form ```-t refs/lethe/my_branch``` for each
parent ref of the form ```refs/heads/my_branch```, and ```-t refs/lethe/my/refpath``` for non-head
refs of the form ```refs/my/refpath```. All provided parent refs *and* any dereferenced parent refs
are used to generate default target refs.
If any of the target refs already exist, the commits they point to become parents of the created commit.
- ```-m "my message"``` sets the commit message for the snapshot. By default, "snapshot <current datetime>" is used. 
- ```-r path/to/repo``` can be provided to specify a repository outside of the current working directory.

```bash
$ cd path/to/repo
$ git branch
* master
$ lethe
```
is equivalent to
```bash
lethe -r path/to/repo -p HEAD
```
or
```bash
lethe -r path/to/repo -p HEAD -p refs/heads/master -t refs/lethe/HEAD -t refs/lethe/master
```

### Creating a commit programmatically
```python
import lethe
REPO = '/path/to/repo'

commit_sha = lethe.snap(cwd=REPO)
tree_sha = lethe.get_tree(commit_sha, cwd=REPO)

print('Created new commit with hash ' + commit_sha + ' aka refs/lethe/HEAD')
print('Code (tree) state is ' + tree_sha)
```


## Installation

Requirements:
* python 3 (written and tested with 3.6)
* git (accessible on the system ```PATH```)

Install with pip:
```bash
pip install lethe 
```
