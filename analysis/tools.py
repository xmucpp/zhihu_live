# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 00:04:12 2017

@author: Lily
"""
# the analyse of data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# describe
def describe_data():
    df_end.describe().to_csv('des_end.csv')
    df_ongo.describe().to_csv('des_ongo.csv')


# Visualization
def box_plot(df,a):
    plt.show(sns.boxplot(df[a],width=0.5))


def jointplot(df,x,y):
    df1 = df.loc[:,[x,y]]
    df1 = df1.dropna()
    sns.jointplot(x,y,df1,kind='reg')
    plt.show()

    
def histogram(df,a):
    df_a = df[a].dropna()
    print df_a
    plt.figure()
    sns.distplot(df_a,bins=100,rug=True)
    plt.show()
    
    
# regression analysis
def regression_analysis(df):
    print df.corr()