# Master_thesis_project

Thanks in advance to everyone that participates in this project for my master thesis.
In order to participate in the survey, having python installed on your personal computer IS REQUIRED! You can install it from the following link https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe
Instructions on how to create a virtual environment to run the survey will be presented later.

This project aims at collecting data about choices of features for a Both Hands vs. Both Feet motor imagery classification.
In particular, by inspecting images reporting ERD/ERS spectrograms and Fisher's scores features maps calculated starting from the signal PSD, the goal is to select the features ( frequency-channel pairs) that you consider the most valuable (emergent or stable for example) and discriminative in order to train a classifier for that specific subject based on the analyzed sample.

Examples of the images that will be shown when using the program can bee seen by looking at the files inside the folder "images_dataset"

The final goal of the project is to use the knowledge of experts of the field to try and develop a model for the automatic selection of features using the same kind of images that are proposed during the survey.

In order to participate you will need to download this github folder by clicking on the code button and then download zip (see following image for visual example), the download can take a while to complete due to the size of the folder.
![img_download_from_github](https://github.com/user-attachments/assets/3a350d7d-9a02-4059-b979-7048b87c80d6)


Once you downloaded the zip file, you will need to extract its content(it will take a moment since it contains also the dataset with the images for the program to run) and it should look like in the image below.
![folder structure](https://github.com/user-attachments/assets/8e800296-2c81-42fd-b134-37abc1ac2ebe)

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
   if you receive an error after using the .\env\Scripts\activate command, telling you that the system does not let you run scripts, you can use the following command to solve the problem
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
Don't worry if the program doesn't start immediatly, the first time it is launched it can take 1 minute to start

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
Don't worry if the program doesn't start immediatly, the first time it is launched it can take 1 minute to start

The program should now be running and you should be able to take the survey and at the end you can report your results by sending the auto-generated "final_results.txt" file using the survey at the Answer link below, where you can also report any problem encountered when trying to take the survey.

Answer link: https://suncake.com/v/2b617e23

This section will contain useful instructions on how to use the program for the survey

- The first screen that you will see is a brief recap of what is already said in this Github page and should look like this
![initial screen](https://github.com/user-attachments/assets/e4388d59-5c9e-424d-aa5c-7ea8e62424c0)

- Once you have read the instructions or if you already know how the program works, you can proceed to the actual survey by pressing the ENTER key

- If everything works correctly, you will now see a screen similar to the one reported in the picture below
![survey screen](https://github.com/user-attachments/assets/28aa5276-4462-4c7b-a091-5d0d8bc92a9a)


- The images of the Features maps shown on screen are 4, one for each of the time window (equal lenght) in which the continuous feedback period was split into. The image below clarifies the time sequence of the 4 windows
![window order](https://github.com/user-attachments/assets/6b1b38fb-198b-4aa9-aee5-e470e7883c38)

- An interactive grid is placed on the bottom right side of the screen and it will let you select all the features (channel-frequency pairs) that you consider to be important and useful for discriminating between the Both Hands and Both Feet tasks.
- To help you in the selection of the features, the program will let you see the ERD/ERS spectrograms for the Both Hands and Both Feet tasks for each individual channel. In order to tell the program which channels to show, you will need to select the cells with the corresponding channel label in the 4x4 grid on the top-right side of the window. Once you selected the channels you are interested in, you need to click the button "Show ERD/ERS spectrograms of selected channels". To make it easy to see which channels you have selected on the 4x4 grid, the selected cells will turn green as in the example picture below.

![seleceted channels](https://github.com/user-attachments/assets/72547a13-375d-4e67-9292-dad6abc5204e)

- Considering the large amount of images that can appear on screen, the button "close all images" can be used to close all the windows showing the images

- Once you are sure about the features you have seleceted for that specific sample, you can save them and go ahead with the next sample by pressing the ENTER key

- After each evaluated sample, the program automatically writes the results on the "final_results.txt" file. This lets you close the program earlier if you do not have time to analyze all the 20 samples that are proposed every time that the survey is taken.

-After the last sample of the batch is evaluated, the program will automatically close and close all the windows opened by it.

- The survey can be taken multiple times and it will show different random samples every time the program is launched since there is a file that keeps track of the samples that were already analyzed. If you want to analyze again samples that you have already seen, simply delete the "already_done.txt" file that is located in the same folder of the program

- If there are no more new samples to analyze, the initial screen of the program will clearly tell you that as can be seen in the below image for reference.
![final screen](https://github.com/user-attachments/assets/349c40ff-80a4-4c5b-b984-79b96572df00)

- At the end, to complete the survey you will need to send the "final_results.txt" file using the Answer link (https://suncake.com/v/2b617e23) where you can also report any problems with the program (feedback is highly appreciated)

