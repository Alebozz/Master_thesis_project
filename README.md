# Master_thesis_project
Thanks in advance to everyone that participates in this project for my master thesis.\n
In order to participate in the survey, having python installed on your personal computer IS REQUIRED! You can install it from the following link https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe
Instructions on how to create a virtual environment to run the survey will be presented later.

This project aims at collecting data about choices of features for a Both Hands vs. Both Feet motor imagery classification.
In particular, by inspecting images reporting ERD/ERS spectrograms (computed using Welch's method), ERD/ERS topoplots over time and Fisher's scores features maps calculated starting from the signal PSD, the goal is to select the features ( frequency-channel pairs) that you consider the most valuable and discriminative in order to train a classifier for that specific subject.

Examples of the images that will be shown when using the program can bee seen by looking at the files inside the folder "images_datasets_merged"

The final goal of the project is to use the knowledge of experts of the field to try and develop a model for the automatic selection of features using the same kind of images that are proposed during the survey.

In order to participate you will need to download this github folder by clicking on the code button and then download zip (see following image for visual example)
![img_download_from_github](https://github.com/user-attachments/assets/4d13510a-d4cb-468e-a2e2-e4a80bff5373)

Once you downloaded the zip file, you will need to extract its content(it will take a while since it contains also the dataset with the images for the program to run) and it should look like in the image below.
![folder sample](https://github.com/user-attachments/assets/1e2d9a30-4f39-4752-93d4-c316f3084f18)


Then, based on your Operating System you will need to use the following commands on the command terminal:

--Windows Operating System instructions--
1) To open the command terminal, place yourself inside the folder that you extracted as it is shown in the previous image
2) then press alt+d and then write 'cmd' (without the '') and press the enter button; Alternatively, you can hold shift and press the right click mouse button and select the 'open in terminal' or the 'powershell' option
3) now, in order to create the virtual environment to run the python script you will need to enter the following commands in the same order as they are presented:
   ```console
   python -m venv env
   ```
   ```console
   .\env\Scripts\activate
   ```
   if you receive an error after using the .\env\Scripts\activate command, telling you that the system does not let you run scripts, you can use the following commands to solve the problem
   ```console
   Set-ExecutionPolicy Unrestricted -Scope Process
   ```
   ```console
   .\env\Scripts\activate
   ```
   After that you can proceed with the following command to set up the virtual environment in order to run the program. To do so, use the following command in the command terminal
   ```console
   pip install -r requirements.txt
    ```
5) The virtual environment should be correctly set up now and the program can be executed using the following command on the command terminal
  ```console
  python survey_v1.0.py
  ```
Don't worry if the program doesn't start immediatly, the first time it is launched it can take 1 or 2 minutes to start

--Linux Ubuntu Operating System instructions--
1) To open the command terminal, place yourself inside the folder that you extracted
2) press the right mouse button and open a terminal window
3) now, in order to create the virtual environment to run the python script you will need to enter the following commands in the same order as they are presented:
   ```console
   python -m venv env
   ```
   ```console
   source env/bin/activate
   ```
   ```console
   pip install -r requirements.txt
   ```
4) The virtual environment should be corretly set up now and the program can be executed using the following command on the command terminal
  ```console
  python survey_v1.0.py
  ```
Don't worry if the program doesn't start immediatly, the first time it is launched it can take 1 or 2 minutes to start

The program should now be running and you should be able to take the survey and at the end you can report your results by sending the auto-generated "final_results.txt" file using the survey at the Answer link below, where you can also report any problem encountered when trying to take the survey.

Answer link: PUT HERE LINK TO THE ACTUAL SURVEY https://suncake.com/v/2b617e23

This section will contain useful instructions on how to use the program for the survey

- The first screen that you will see is a brief recap of what is already said in this Github page and should look like this
![initial screen](https://github.com/user-attachments/assets/0f327940-b47c-4306-96f3-47b35b3705cc)

- Once you have read the instructions or if you already know how the program works, you can proceed to the actual survey by pressing the ENTER key

- If everything works correctly, you will now see a screen similar to the one reported in the picture below
![main screen sample](https://github.com/user-attachments/assets/3625292c-4e9d-40ae-8d3c-ebe4ecf2b823)

- The images of the Features maps on the top part of the window can be 2 or 3 and report the Fisher's scores for the single runs performed by the subject
- The image on the bottom part corresponds to the Fisher's score Feature map of the concatenation of the individual runs.
- On top of it, an interactive grid is placed and it will let you select all the features (channel-frequency pairs) that you consider to be important and useful for discriminating between the Both Hands and Both Feet tasks.
- To help you in the selection of the features, the program will let you see the ERD/ERS topoplots over time for the mu and beta band separately by simply clicking on the buttons "show mu band topoplots" and "show beta band topoplots" respectively. In case of problems in determining the channels on the scalp for the topoplot, a reference image can be visualized by clicking on the button "show channels positions in topoplot".
- Another type of data that the program lets you visualize is the ERD/ERS spectrograms for the Both Hands and Both Feet tasks for each individual channel. In order to tell the program which channels to show, you will need to select the cells with the channel label in the 4x4 grid on the right side of the window. Once you selected the channels you are interested in, you need to click the button "Show ERD/ERS spectrograms of selected channels". To make it easy to see which channels you have selected on the 4x4 grid, the selected cells will turn green as in the example picture below
- A particular kind of data that is shown for both the topoplots and the spectrograms is the difference of the ERD/ERS values(Both_Hands - Both_Feet) for the two tasks. These type of plots have positive and negative values. Higher is the distance of a value from zero in both directions (negative or positive doesn't matter), higher is the discriminancy between the two motor imagery tasks for the channel(in case of a topoplot) or for the channel-frequency pair in the case of the spectrograms

![channels selection sample](https://github.com/user-attachments/assets/30359697-d5bf-43d9-a558-10afd5d73866)

- Considering the large amount of images that can appear on screen, the button "close all opened images" can be used to close all the windows showing the images

- Once you are sure about the features you have seleceted for that specific sample, you can save them and go ahead with the next sample by pressing the ENTER key

- After each evaluated sample, the program automatically writes the results on the "final_results.txt" file. This lets you close the program earlier if you do not have time to analyze all the 20 samples that are proposed every time that the survey is taken.

-After the last sample of the batch is evaluated, the program will automatically close and close all the windows opened by it.

- If you want, you can retake the survey as many times as you want since it randomly selects the samples to evaluate each time the program is launched. Also, the results of each execution of the program will be saved on the same "final_results.txt" file by appending the latest results to the ones already generated by previous runs.

- At the end, to complete the survey you will need to send the "final_results.txt" file using the Answer link (https://suncake.com/v/2b617e23) where you can also report any problems with the program (feedback is highly appreciated)

