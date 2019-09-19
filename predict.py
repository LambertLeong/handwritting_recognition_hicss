'''
This code is for real-time predictions.
run_hardware.ino needs to be running in arduino studio before starting this program
by Lambert Leong
'''

import serial  # sudo pip install pyserial should work
import os
import argparse
from argparse import RawTextHelpFormatter
import sys
import math
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score , make_scorer,accuracy_score
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.externals import joblib

def process_file(csv_file):
	file_df = pd.read_csv(csv_file)
	file_df.columns=['time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz',' ']
	calc = np.array([0,0,0,0,0,0])
	for i, row in file_df.iterrows():
		record = np.array([])
		v = []
		d = []
		if i == 0:
			continue
		for j in range(1,4):
			a_0 = file_df.iloc[i-1, j]
			a_i = file_df.iloc[i,j]
			v_tmp = (a_0 + a_i)/2.0*row[0]
			d += [v_tmp*row[0]]
			v += [v_tmp]
		record = np.array(v+d)
		calc = np.vstack((calc, record))
	new_df = pd.DataFrame(calc[1:,:], columns=['vx', 'vy', 'vz','dx', 'dy', 'dz'], dtype=float)
	### distance
	dx = new_df['dx'].sum()
	dy = new_df['dy'].sum()
	dz = new_df['dz'].sum()
	### velc
	min_vx = new_df['vx'].min()
	max_vx = new_df['vx'].max()
	mean_vx = new_df['vx'].mean()
	min_vy = new_df['vy'].min()
	max_vy = new_df['vy'].max()
	mean_vy = new_df['vy'].mean()
	min_vz = new_df['vz'].min()
	max_vz = new_df['vz'].max()
	mean_vz = new_df['vz'].mean()
	### acc
	min_ax = file_df['ax'].min()
	max_ax = file_df['ax'].max()
	mean_ax = file_df['ax'].mean()
	min_ay = file_df['ay'].min()
	max_ay = file_df['ay'].max()
	mean_ay = file_df['ay'].mean()
	min_az = file_df['az'].min()
	max_az = file_df['az'].max()
	mean_az = file_df['az'].mean()
	### gyro
	min_gx = file_df['gx'].min()
	max_gx = file_df['gx'].max()
	mean_gx = file_df['gx'].mean()
	min_gy = file_df['gy'].min()
	max_gy = file_df['gy'].max()
	mean_gy = file_df['gy'].mean()
	min_gz = file_df['gz'].min()
	max_gz = file_df['gz'].max()
	mean_gz = file_df['gz'].mean()

	total_d = (dx*dx + dy*dy + dx*dz)**(.5)
	return_np = np.array([dx, dy, dz, total_d,
	min_vx, max_vx, mean_vx,
	min_vy, max_vy, mean_vy,
	min_vz, max_vz, mean_vz,
	min_ax, max_ax, mean_ax,
	min_ay, max_ay, mean_ay,
	min_az, max_az, mean_az,
	min_gx, max_gx, mean_gx,
	min_gy, max_gy, mean_gy,
	min_gz, max_gz, mean_gz]
	)
	return return_np

### GLOBALS ###
clf = joblib.load('hand_writing_xgb.pkl')
print('\nModel Loaded\n')
serial_port = "/dev/ttyUSB0"
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

if __name__ == '__main__':
	#argv = parse_arguments()
	#if argv.num == 0:
	#	out_dir = to_dir+str(argv.num)+"/"
	#else:
	#	out_dir = to_dir+str(argv.num)+"/"
	#print"\n\n File writting to "+ out_dir+"\n\n"
	#to_dir = "data/"

	out_dir = ""
	num_files = len([f for f in os.walk(out_dir).next()[2] if f[-4:] == ".csv"])
	num_files= 0 #= len([f for f in os.walk(out_dir).next()[2] if f[-4:] == ".csv"])
	count = num_files+1
	exit = 0
	listen = 0
	ser = serial.Serial(serial_port, baud_rate)
	while exit < 1:
		print( "Ready to record!!!")
		out_line = ""
		line = ser.readline()
		line = line.decode("utf-8") #ser.readline returns a binary, convert to string
		if "START" in line:
			listen = 1
			print( "Start writing digit ")#+str(argv.num))
			#print "Start writing digit "+str(argv.num)
		while( listen > 0):
			line = ser.readline()
			line = line.decode("utf-8") #ser.readline returns a binary, convert to string
			if "STOP" in line:
				listen = 0
				#print "writing file "+out_dir+str(count)
				print("\n"+out_line[-40:]+"\n")

				###### process and predict #####
				test_file = "tmp/tmp.csv"
				file = open(test_file,'w+')
				file.write(out_line)
				file.close()
                                
                                ### Inefficient to perform I/O here. A quick solution so that this runs smooth on most systems ###
				data = np.array(process_file(test_file))
				data = data.transpose()
				data_df = pd.DataFrame(data=[data])
				#print(data.shape)
				pred = clf.predict(data_df.values)
				print('\n\nprediction = '+str(pred)+'\n\n')
				count+=1
			out_line+=line
