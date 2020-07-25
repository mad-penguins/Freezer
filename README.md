# Freezer
**Freezer** is a lightweight HTML template engine. Now you don't need to manually create many similar html pages. Freezer will do it for you. You only need to specify the content of *snowflakes* and their location in the project.

## Getting started
How to use this template engine in your site project? Quite easy. Now let's look at the currently implemented Freezer connectivity options:

* #### Adding Freezer as submodule to your repository (recommended)
  > Your site project must be in a git repository. Freezer was designed to be included in a project as a git-submodule.
  > Freezer may be available in pip storage in the future.

  In different git GUI clients, connecting submodules can be implemented in different ways. Let's have a look at the old and reliable method: console git client.
  
  ```bash
  $ git submodule add https://github.com/mad-penguins/Freezer.git
  $ git commit -m "Add Freezer as a submodule"
  ```
  > **Advantage**: you can always easily update *Freezer* to the latest version:
  > 
  > ```bash
  > $ git submodule update
  > ```
  
  Next, create a new Freezer project:
  
  ```bash
  $ python3 Freezer/freezer.py start NameYourProject
  ```
  
  > Note that the file tree in the repository will look like this:
  > - **Your_project_Folder**
  >     - |-  **.git**
  >     - |-  **conf**
  >     - |-  **Freezer**
  >        - |-  *.git*
  >        - |-  *.gitignore*
  >        - |-  *freezer.py*
  >        - |-  *LICENSE*
  >        - |-  *README.md*
  >     - |-  **py**
  >     - |-  **snow**
  >     - |-  **src**
  >     - |-  **static**
  >     - |-  **var**
  >     - |-  *.gitmodules*
  >     - |-  *NameYourProject.freezer*
  >
  > Note: files which name begins with a dot can be hidden by `ls` command or your file manager.
  
  
* #### Adding Freezer as python script to your project
  Just download the file `freezer.py` from the master branch and paste it into root your project directory.
  
  > **Advantage**: you don't need to create a repository for your project.
  >
  > **Disadvantage**: to update *Freezer*, you will have to download the file again and replace it in the project.
  
  Next, create a new Freezer project:
  
  ```bash
  $ python3 freezer.py start NameYourProject
  ```
  
  > Note that the file tree in the repository will look like this:
  > - **Your_project_Folder**
  >     - |-  **conf**
  >     - |-  **py**
  >     - |-  **snow**
  >     - |-  **src**
  >     - |-  **static**
  >     - |-  **var**
  >     - |-  *freezer.py*
  >     - |-  *NameYourProject.freezer*
  >
  > Note: files which name begins with a dot can be hidden by `ls` command or your file manager.
  
## Create your first html pages
*Under construction...*

## Commands

```start``` - create a new Freezer`s project.

```update``` - update path Snowflakes.

```build``` - building and export project.
