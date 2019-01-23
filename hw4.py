import pandas as pd
import numpy as np
import sqlite3, os
def csv_to_dataframe(filename):
    df = pd.read_csv(filename,decimal=",",index_col=0)
	#df = pd.read_csv('countries_of_the_world.csv',decimal=",", index_col = 0)
    return df

def format_df(df):

#This function takes a countries DataFrame as created by the previous function

    list1 =[]
    df['Region'] = df['Region'].str.title()
    df['Region'] = df['Region'].str.strip()
    for i in range(len(df.index)):
        list1.append(df.index[i].strip())
    df.index = list1
def growth_rate(df):
	newdf1_bt = df[["Birthrate"]]
	newdf1_dt = df[["Deathrate"]]
	new_col = newdf1_bt - newdf1_dt.values
	df['Growth Rate'] = new_col
	
	
	
def dod(p, r):
	num_yrs = 0
	while p > 2:
		p = p + p * r / 1000
		num_yrs += 1
	return num_yrs
	
def years_to_extinction(df):

#This function takes a formatted countries DataFrame that has a Growth Rate column and adds a column labeled 'Years to Extinction'. 

	df['Years to Extinction'] = np.nan
	for index in df.index:
		if df.loc[index,'Growth Rate'] < 0:
			df.loc[index, 'Years to Extinction'] = dod(df.loc[index, 'Population'], df.loc[index, 'Growth Rate'])
			
def dying_countries(df):

# This function takes a formatted countries DataFrame that has a Years to Extinction column and returns a Series whose labels are the countries with negative growth rates and whose values are the number of years until they're dead in sorted order from first to last to die

	result = pd.Series(df['Years to Extinction'].dropna())
	return result.sort_values()
def class_performance(conn,tbl_name="ISTA_131_F17"):

#This function takes a connection object and a table name with default value of "ISTA_131_F17" and returns a dictionary that maps the grades (capitalized) to their 1-decimal point precision percentages of the class that got that grade

	
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    dic = {}
    string = []

    query1 = "SELECT COUNT(*) FROM " +tbl_name +";"
    total = c.execute(query1).fetchone()[0]
    
    query2 = "SELECT UPPER(grade), COUNT(*) FROM " + tbl_name + " GROUP BY grade;"
    grade = c.execute(query2).fetchall()
    for i in range(len(grade)):
        dic[grade[i][0]] = round((grade[i][1] / total) * 100,1)

    return dic
def improved(conn,tbl_name1, tbl_name2):

#This function takes a connection object, two table name and returns
#a sorted list of the last names of the students that did better in the class
#represented by the second table than they did in the first.

    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stud_list = []

    query1 = "SELECT " + tbl_name1 + ".last FROM " + tbl_name1 +" INNER JOIN "\
    + tbl_name2 + " ON " +tbl_name1+".last = " + tbl_name2 + ".last AND " + tbl_name1 +\
    ".id = " + tbl_name2 + ".id WHERE " + tbl_name1+".grade < "\
    + tbl_name2 + ".grade ORDER BY " + tbl_name1 + ".last;"
    for stu in c.execute(query1).fetchall():
        stud_list.append(stu[0])
    return stud_list

def main():

#This main function creats a frame from "countries_of_the_world.csv", adds
#Growth Rate and Years to Extinction columns, and prints the top 5 dying countries.

    df = csv_to_dataframe("countries_of_the_world.csv")
    format_df(df)
    growth_rate(df)
    years_to_extinction(df)
    ans = dying_countries(df)
    for i in range(5):
        print(ans.index[i] + ": " + str(ans[ans.index[i]]) + " Years to Extinction")
main()

	

			
		