import os
import numpy as np
import random

#These are the constraints or rather the operations to be followed in minisat
def constraints(f):
	E = np.zeros(shape=(81,81))
	lines = 0

	for i in range(81):
	    row1 = i/9
	    col1 = i%9

	    for j in range(81):
		row2 = j/9
		col2 = j%9

		#vertices in same row, same column and same box are connected
		if row1==row2 or col1==col2 or ((row1/3)==(row2/3) and (col1/3)==(col2/3)) :
			E[i][j] = 1
		
		#diagonal vertices are connected		
		if (row1==col1 and row2==col2) or (row1+col1==8 and row2+col2==8):
			E[i][j]=1
		
		#a vertex can't be connected to itself
		if i==j:
		    	E[i][j] = 0

	#Each vertex is assigned a color	
	for v in range(81):
	    for color in range(9):
		f.write(str(v+1) + str(color+1) + " ")
	    f.write(" 0\n")
	    lines = lines + 1

	#Every vertex is given exactly one color
	for v in range(81):
	    for i in range(9):
		for j in range(i+1,9):
		    f.write("-" + str(v+1) + str(i+1) + " -" + str(v+1) + str(j+1) + " 0\n")
		    lines = lines + 1

	#Two connected vertices don't have same color
	for v1 in range(81):
	    for v2 in range(81):
		 if E[v1][v2]==1:
		     for i in range(9):
		         f.write("-" + str(v1+1) + str(i+1) + " -" + str(v2+1) + str(i+1) + " 0\n")
		         lines = lines + 1
	
	return lines;

#Function to solve sudoku where minisat command is called in terminal
def solve_sudoku(lines):
	f = open("sat_in.txt", "r")
	temp = f.read()
	f.close()

	f = open("sat_in.txt", "w")
	f.write("p cnf 819 " + str(lines) + "\n")

	f.write(temp)
	f.close()

	os.system("minisat sat_in.txt sat_out.txt")

	output = open("sat_out.txt", "r")
	lines_list = output.readlines()

	out = np.zeros(shape=(9,9))
	
	for val in lines_list[1].split():
	    data = int(val)

	    if(data>0):
		vertex = data/10 - 1
		digit = data%10
		row = vertex/9
		col = vertex%9
		out[row][col] = digit

	output.close()

	return out;

def print_sudoku(matrix):
	print ("\n \n****************** SUDOKU++ ******************")
	for v1 in range(9):
		for v2 in range(9):
			if(matrix[v1][v2]==0):
				print ".",
			else:
				print int(matrix[v1][v2]),
		print ""
	
	return;

x = input("Enter your choice: \n1 - to generate a solved sudoku\n2 - to solve a sudoku\n3 - to generate a sudoku\n")

if(x==1):
	f = open("sat_in.txt", "w+")
	lines = constraints(f)

	#Extra constrain to get new sudoku each time, by fixing the value of a random element by a random number
	random1 = random.randint(1,81)
	random2 = random.randint(1,9)
	f.write(str(random1) + str(random2) + " 0\n")
	lines=lines+1
	f.close()
	print_sudoku(solve_sudoku(lines))


if(x==2):
	#input	
	M = np.zeros(shape=(9,9))
	name_of_file = raw_input("Enter name of the file :\n")
	sudoku = open(name_of_file,"r")
	lines_list = sudoku.readlines()
	for i in range(9):
		for j in range(17):
			if (j%2)==0:
				if(lines_list[i][j]=='.'):
					M[i][j/2]=0
				else:
					M[i][j/2]=int(lines_list[i][j])

	f = open("sat_in.txt", "w+")
	lines = constraints(f)

	#Adding the contraints of given sudoku, i.e. adding the colors of vertices, which is given to us
	for v in range(9):
		for v1 in range(9):
			if(M[v][v1]!=0):
				f.write(str(v*9 + v1 + 1)+str(int(M[v][v1]))+" 0\n")
				lines = lines + 1

	f.close()

	print_sudoku(solve_sudoku(lines))


if(x==3):
	f = open("sat_in.txt", "w+")
	lines = constraints(f)
	
	#Extra constrain to get new sudoku each time, by fixing the value of a random element by a random number
	random1 = random.randint(1,81)
	random2 = random.randint(1,9)
	f.write(str(random1) + str(random2) + " 0\n")
	lines=lines+1
	f.close()

	#generate already solved sudoku	
	pre_sudoku = solve_sudoku(lines)
	
	out = np.zeros(shape=(9,9))
	outp = np.zeros(shape=(9,9))	

	#pre_sudoku is copied in "out" and "outp" and changes are made to them
	for row in range(9):
		for col in range(9):
			out[row][col] = pre_sudoku[row][col]
			outp[row][col] = pre_sudoku[row][col]
	
	while(True):
		rand_vertex = random.randint(0,80) #we will remove this vertex
		roww = rand_vertex/9
		coll = rand_vertex%9
		
		if(out[roww][coll]!=0):
			out[roww][coll] = 0
			f = open("sat_in.txt", "w")
			lines = constraints(f)

			#Add the negation of this removed vertex in our constraints. If we still get another solution after its negation, then we would stop there. While if we don't get a solution, that means we have reached unique solution's stage
			for v in range(81):
			    	row1 = v/9
			    	col = v%9
				element = int(pre_sudoku[row1][col])
			    	if out[row1][col] != 0:
		    			f.write(str(v+1)+str(element)+" 0\n")
		    			lines = lines + 1
		    		elif out[row1][col]==0 and row1==roww and col==coll:
		    			f.write("-"+str(v+1)+str(element)+" 0\n")
		    			lines = lines + 1

			f.close()

			f = open("sat_in.txt", "r")
			temp = f.read()
			f.close()

			f = open("sat_in.txt", "w")
			f.write("p cnf 819 " + str(row) + "\n")

			f.write(temp)
			f.close()

			os.system("minisat sat_in.txt sat_out.txt")

			output = open("sat_out.txt", "r")
			lines_list = output.readlines()
			if(lines_list[0][0] =="S"):
				break

	flag=0
	
	#Checking for minimal solution
	while(flag==0):
		t = np.arange(0, 81, 1)                  
		random.shuffle(t)			 #traversing through the array in random order to get minimal sudoku
		for vertex in range(81):
			v1 = t[vertex]/9
			v2 = t[vertex]%9
			if(outp[v1][v2]!=0):
				val = outp[v1][v2]
				outp[v1][v2] = 0

				f = open("sat_in.txt","w")

				lines = constraints(f)

				for v in range(81):
				    	row1 = v/9
				    	col = v%9
					element = int(pre_sudoku[row1][col])
				    	if outp[row1][col] != 0:
			    			f.write(str(v+1) + str(element) + " 0\n")
			    			lines = lines + 1
			    		elif outp[row1][col]==0 and row1==v1 and col==v2:
			    			f.write("-" + str(v+1) + str(element) +" 0\n")
			    			lines = lines + 1

				f.close()

				f = open("sat_in.txt", "r")
				temp = f.read()
				f.close()

				f = open("sat_in.txt", "w")
				f.write("p cnf 819 " + str(lines) + "\n")

				f.write(temp)
				f.close()

				os.system("minisat sat_in.txt sat_out.txt")

				output = open("sat_out.txt", "r")
				lines_list = output.readlines()
				if(lines_list[0][0] == "S"):
					outp[v1][v2] = val


		flag=1
	
	print_sudoku(outp)
