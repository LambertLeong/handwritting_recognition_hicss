'''
This code is for processing the multiple csv files output during recording

by Lambert Leong
'''

import sys
import os
import math
import pandas as pd
import numpy as np

df = pd.DataFrame({'dx':[], 'dy':[], 'dz':[], 'total_d':[], 'min_vx':[],
'min_vy':[], 'min_vz':[], 'min_ax':[], 'min_ay':[], 'min_az':[], 'min_gx':[],
'min_gy':[], 'min_gz':[], 'max_vx':[], 'max_vy':[], 'max_vz':[], 'max_ax':[],
'max_ay':[], 'max_az':[], 'max_gx':[], 'max_gy':[], 'max_gz':[],
'mean_vx':[], 'mean_vy':[], 'mean_vz':[], 'mean_ax':[], 'mean_ay':[],
'mean_az':[], 'mean_gx':[], 'mean_gy':[], 'mean_gz':[] })

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

directory = 'data/'

master = np.array([
100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,
100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,
100.0,100.0,100.0,100.0,100.0,100.0,100.0,100.0,
100.0,100.0,100.0,100.0,100.0,100.0,100.0#,100.0
])
headers = ['dx', 'dy', 'dz', 'total_d',
'min_vx','max_vx', 'mean_vx',
'min_vy','max_vy','mean_vy',
'min_vz','max_vz','mean_vz',
'min_ax','max_ax', 'mean_ax',
'min_ay','max_ay','mean_ay',
'min_az','max_az','mean_az',
'min_gx','max_gx','mean_gx',
'min_gy','max_gy','mean_gy',
'min_gz','max_gz','mean_gz']
labels = []

for direct in os.listdir(directory):
	label_dir = directory+direct+'/'
	if not(direct is '0' or direct is '1'):
		continue
	for filename in os.listdir(label_dir):
		test_record = []
		csv_file = label_dir+filename
		test_record = process_file(csv_file)
		if direct is '0':
			labels += [0]
		elif direct is '1':
			labels += [1]
		master = np.vstack((master,test_record))
labels = np.array(labels)
labels = labels.transpose()
master_df = pd.DataFrame(master[1:,:],columns=headers)
master_df['label'] = labels
print(master_df.head())
master_df.to_csv('master_handwriting_data.csv', encoding='utf-8')
sys.exit(0)
