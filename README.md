# Repo Overview

This repo houses the code used to gather and analyze the data presented in a manuscript which was accepted to Hawaii International Conference on Science Systems [(HICSS)](https://hicss.hawaii.edu) 

### Summary

We developed custom hardware to measure wrist movement, like a smart watch or wearable IOT device, during writing.  We were able to analyze the data and build a machine learning classifier that can identify the digit, zero or one, being written.  The code for the hardware, analysis, and model are located in this repo.

For more information contact [Lambert Leong](lambert3@hawaii.edu) 

## Hardware and Code

* The [ESP32 feather]([https://www.adafruit.com/product/3405](https://www.adafruit.com/product/3405)) micro-controller board was used to capture the data.

* The [LSM9D1]([https://www.sparkfun.com/products/13762](https://www.sparkfun.com/products/13762)) IMU housed the accelerometer and gyroscope used to capture the wrist movements. 

* run_hardware.ino contains the code that runs the hardware.  Code needs to be run in arduino ide and must be started up before any analysis or before runing any of the resulting python code.

* Eagle file describing the layout is to come.

## Capture Code

* After starting the run_hardware.ino code, in the command-line, run the record.py code.  Input the appropriate command-line arguments.  The program will prompt you when it is ready to record wrist motion.  Press the button on the device to start writing and press it again to end writing.  It will prompt you when and where the output file is saved to and when it is ready for the next recording.

## Analysis Code

* process.py - Code used to parse and compile raw output data into a master csv table.
* vis.py - Data used to plot, in 3D, the top 3 principal components against each other.
* vis_data.csv - a sub-set of actual data.  Used for example purposes.

## Real Time Prediction Code

* predict.py - This code loads the pickled model, records data stream from the device, and predicts the number being written in real time.  run_hardware.ino needs to started up before starting up prediction code.

## Model
A pickle file of the model can be download and run.  It can classify the written digits zero and one.  The file is titled hand_writing_xgb.pkl
