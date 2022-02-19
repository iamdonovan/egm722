[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/iamdonovan/egm722/main)

# EGM722: Programming for GIS and Remote Sensing Exercises

## 1. Getting started

To get started with the exercises, you'll need to install both `git` and `conda` on your computer. You can follow the
instructions provided on Blackboard, or from the instructions for installing git from [here](https://git-scm.com/downloads), 
and Anaconda from [here](https://docs.anaconda.com/anaconda/install/). 

## 2. Download/clone this repository

Once you have these installed, __clone__ this repository to your computer by doing one of the following things:

1. Open GitHub Desktop and select __File__ > __Clone Repository__. Select the __URL__ tab, then enter the URL for this 
   repository.
2. Open __Git Bash__ (from the __Start__ menu), then navigate to your folder for this module.
   Now, execute the following command: `git clone https://github.com/iamdonovan/egm722.git`. You should see some messages
   about downloading/unpacking files, and the repository should be set up.
3. You can also clone this repository by clicking the green "clone or download" button above, and select "download ZIP"
   at the bottom of the menu. Once it's downloaded, unzip the file and move on to the next step. I don't recommend this
   step, however, as it will be more difficult for you to download the material for each week. 

## 3. Create a conda environment

Once you have successfully cloned the repository, you can then create a `conda` environment to work through the exercises.

To do this, use the environment.yml file provided in the repository. If you have Anaconda Navigator installed,
you can do this by selecting __Import__ from the bottom of the __Environments__ panel. 

Otherwise, you can open a command prompt (on Windows, you may need to select an Anaconda command prompt). Navigate
to the folder where you cloned this repository and run the following command:

```
C:\Users\iamdonovan> conda env create -f environment.yml
```

This will probably take some time (so feel free to catch up on Facebook or whatever kids do nowadays), but fortunately 
you will only have to do this once. If you

## 4. Start jupyter-notebook

From Anaconda Navigator, you can launch jupyter-notebook directly, and navigate to the folder where the first week's
practical material is located. Make sure that your egm722 environment is activated.

From the command-line, first open a terminal window or an __Anaconda Prompt__, and navigate to the folder where the
first week's practical material is located.

Activate your newly-created environment (`conda activate egm722`). Launch jupyter-notebook (`jupyter-notebook.exe`),
which should launch a web browser window, which should give you an overview of the current folder. 

## 5. Next steps
The material for this module is organized as follows:

Week 1. Introduction to git and programming with python
Week 2. More introduction to python
Week 3. Working with vector data in python
Week 4. Working with raster data in python
Week 5. Additional exercises

You are free to work through the material at your own pace. If you are enrolled in EGM722 at Ulster University, you
will find additional resources via the module webpage on Blackboard.
