# Master_thesis_project
Thanks in advance to everyone that participates in this project for my master thesis.

This project aims at collecting data about choices of features for a Both Hands vs. Both Feet motor imagery classification.
In particular, by inspecting images reporting ERD/ERS spectrograms (computed using Welch's method), ERD/ERS Scalograms (computed using Matlab cwt function with "Amor" wavelet), ERD/ERS topoplots over time and Fisher's scores features maps calculated starting from the signal PSD, the goal is to select the features ( frequency-channel pairs) that you consider the most valuable and discriminative in order to train a classifier for that specific subject.

Examples of the images that will be shown when using the program can bee seen by looking at the files inside the folder "images_datasets_merged"

The final goal of the project is to use the knowledge of experts of the field to try and develop a model for the automatic selection of features using the same kind of images that are proposed during the survey.

In order to participate you will need to download this github folder by clicking on the code button and then download zip (see following image for visual example)
![img_download_from_github](https://github.com/user-attachments/assets/4d13510a-d4cb-468e-a2e2-e4a80bff5373)

Once you downloaded the zip file, you will need to extract its content(it will take a while since it contains also the dataset with the images for the program to run) and then, based on your Operating System you will need to grab the content of the folder "survey_1_0_OS_NAME" (where OS_NAME stands for your Operative System name ex. Windows or Ubuntu/Linux) and place it in the same folder of all the other files.
After this procedure, your folder should look like this
![folder structure](https://github.com/user-attachments/assets/7c9033bb-5b90-4c40-9cdf-f7a2cda0f011)

Now you can launch the program to take the survey and at the end you can report your results by sending the auto-generated "final_results.txt" file using the survey at the Answer link below, where you can also report any problem encountered when trying to take the survey.

Answer link: PUT HERE LINK TO THE ACTUAL SURVEY

This section will contain useful instructions on how to use the program for the survey

- To launch the program you will need to use the "survey_v1.0" file
- The first screen that you will see is a brief recap of what is already said in this Github page and should look like this
![initial screen](https://github.com/user-attachments/assets/daa2c0af-400b-407c-bafa-9bf813d069c6)

- Once you have read the instructions or if you already know how the program works, you can proceed to the actual survey by pressing the ENTER key

- If everything works correctly, you will now see a screen similar to the one reported in the picture below
![survey screen](https://github.com/user-attachments/assets/a7eff61d-0409-44a7-9e45-08dd272734e4)

- The images of the Features maps on the top part of the window can be 2 or 3 and report the Fisher's scores for the single runs performed by the subject
- The image on the bottom part corresponds to the Fisher's score Feature map of the concatenation of the individual runs.
- On top of it, an interactive grid is placed and it will let you select all the features (channel-frequency pairs) that you consider to be important and useful for discriminating between the Both Hands and Both Feet tasks.
- To help you in the selection of the features, the program will let you see the ERD/ERS topoplots over time for the mu and beta band separately by simply clicking on the buttons "show mu band topoplots" and "show beta band topoplots" respectively. In case of problems in determining the channels on the scalp for the topoplot, a reference image can be visualized by clicking on the button "show channels positions in topoplot".
- Another type of data that the program lets you visualize is the ERD/ERS scalograms for the Both Hands and Both Feet tasks for each individual channel. In order to tell the program which channels to show, you will need to select the cells with the channel label in the 4x4 grid on the right side of the window. Once you selected the channels you are interested in, you need to click the button "Show ERD/ERS scalograms of selected channels". To make it easy to see which channels you have selected on the 4x4 grid, the selected cells will turn green as in the example picture below

![channels_selection_example](https://github.com/user-attachments/assets/5a013ef6-6146-44bd-9910-fcbeece1d6b0)

- Considering the large amount of images that can appear on screen, the button "close all opened images" can be used to close all the windows showing the images

- Once you are sure about the features you have seleceted for that specific sample, you can save them and go ahead with the next sample by pressing the ENTER key

- After the last sample is evaluated, the program automatically generate a "final_results.txt" file reporting all your answers and then the program will close.

- If you want, you can retake the survey as many times as you want since it randomly selects the samples to evaluate each time the program is launched. Also, the results of each execution of the program will be saved on the same "results.txt" file by appending the latest results to the ones already generated by previous runs.

- At the end, to complete the survey you will need to send the "final_results.txt" file using the Answer link () where you can also report any problems with the program (feedback is highly appreciated)

