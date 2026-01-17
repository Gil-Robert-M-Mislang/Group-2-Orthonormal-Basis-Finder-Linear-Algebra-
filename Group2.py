# Library Needed
#
# Numpy Library - Library that contains the function needed for scientific computing of N-Dimensional Array.
# Sympy Library - Library that helps in formatting the output to make it more readable.
# Flask Library - Library that helps in creating the main application by creating a connection between the website files (HTML, CSS, JavaScript).

import numpy as np
import sympy as sp
from flask import Flask, request, jsonify,render_template

# Home Function - Connects the HTML file to the main Python file.
#
# How it works: 
# 1. Initialize app variable to create the flask application instance for the current file.
# 2. Handles the request receive.
# 3. Connects the current python file to the existing HTML file.

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return  render_template("index.html")

# LI_tester - determines if the given matrix is Linearly Independent which is crucial in finding the Orthonormal Basis.
#
# How it works:
# 1. Determines the Shape of the matrix in order to access the row and column size.
# 2. Compares the Rows and the columns
#    (Case 1) If the number of column is less than the number of rows, it immediately returns false saying that the matrix is linearly dependent.
#    (Case 2) If the number of column is equal to the number of rows, it checks for the singularity of the matrix
#               which returns false if the matrix is Singular, otherwise it will return true.
#    (Case 3) If the number of column is greater than the number of rows, it checks for any free variable by comparing its rank to the number of rows
#               If the rank is larger than the number of rows, it will return true. Otherwise, it will return false.

def LI_tester(input):
    size = input.shape

    if size[1] < size[0]:
        return False
    elif size[0] == size[1]:
        determinant = int(np.linalg.det(input))
        if determinant == 0:
            return False

        return True
    else:
        pivot = np.linalg.matrix_rank(input)
        if pivot < size[0]:
            return False

    return True
    
# Sum_Projection - adds all the projection of a given matrix
#                 from the first vector up to the index of 
#                 the vector you're comparing it with.
# How it works:
# 1. Initialize a zero matrix that stores the result of the summation.
# 2. Traverses from 0 to the given index.
# 3. Store the sum of the result of the current index given the formula
#     and the result of the previous index.
# 4. Return the whole result matrix.

def Sum_Projection(input, size, index):
    result_matrix = np.zeros(size[1])

    for i in range(index):
        norm = np.linalg.norm(input[i])
        result_matrix += ((input[index] @ input[i])/ norm**2) * input[i] 

    return result_matrix

# Normalization - normalizes the given matrix
#
# How it works:
# 1. Initialize a empty matrix to store the normalize matrix.
# 2. Traverses through the whole matrix.
# 3. Divide the elements of the current vector by its norm.
# 4. Return the whole resulting matrix.

def Normalization(input, size):
    result_matrix = np.empty(size)

    for i in range(size[0]):
        result_matrix[i] = input[i]/np.linalg.norm(input[i])
    
    return result_matrix

# Gram_Schmidt - responsible for the overall execution of the Gram Schmidt process.
#
# How it works:
# 1. Initialize an empty matrix to store the result of the process.
# 2. Traverses through the whole matrix.
#      (Case 1) If the current vector is the first vector,
#               store the first vector to the result matrix.
#      (Case 2) Otherwise, it stores the difference of the
#               current vector and the sum of its projection.
# 3. Normalizes the result matrix.
# 4. Returns the resulting matrix.

def Gram_Schmidt(input, size):
    result_matrix = np.empty(size)

    for i in range(size[0]):
        if i == 0:
            result_matrix[i] = input[i]
        else:
            result_matrix[i] = input[i] - Sum_Projection(result_matrix, size, i)

    result_matrix = Normalization(result_matrix, size)

    return result_matrix


# Main function - the interface of the program, which consists of the input, process, and output.
#
# How it works: 
# 1. Create a connection between the HTML file and the Python file.
# 2. Store the data given by the JSon file.
# 3. Converts the received data into a matrix,
#    and store its size and its transpose since
#    it needs to be traversed through the columns.
# 4. Checks for the independence of the given matrix.
#       (Case 1) If the matrix is Linearly independent,
#                1. It calls the Gram_Schmidt function to
#                   get the normalized vector.
#                2. It formats the result so that it will be readable.
#                3. it onverts the Matrix into a String List. 
#                4. it returns the string list. 
#       (Case 2) If the matrix is linearly Dependent,
#                   it will produce an error message.

@app.route("/Group2", methods=["POST"])
def main():
    data = request.get_json()

    matrix = np.array(data["matrix"])
    matrix = matrix.T
    matrix_size = matrix.shape

    independence = LI_tester(matrix)
    if independence == True:
            result_matrix = Gram_Schmidt(matrix, matrix_size)

            result_matrix[np.abs(result_matrix) < 1e-12] = 0
            end_matrix = sp.Matrix(result_matrix).applyfunc(sp.nsimplify)
            result_matrix[np.abs(result_matrix) < 1e-12] = 0

            end_matrix = sp.Matrix(result_matrix).applyfunc(
                lambda x: sp.nsimplify(x, tolerance=1e-5, rational=False)
            )

            formatted_result = []
            for i in range(end_matrix.rows):
                row_strings = [str(end_matrix[i, j]) for j in range(end_matrix.cols)]
                formatted_result.append(row_strings)
                
            return jsonify({"result": formatted_result})
    else:

            flag = 0

            return jsonify({"result": flag})


# Runs the current file as a flask application.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
