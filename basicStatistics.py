import math


def maxList(x):
	max_value = x[0]
	for element in x:
		if max_value >= element:
			continue
		else:
			max_value = element
			continue

	return max_value


def sortList(array):
	
	array_to_sort = []
	array_sorted = []
	

	for element in array:
		array_to_sort.append(element)


	

	i = 0


	while i < len(array):
		max_value = maxList(array_to_sort)
		max_value_index = array_to_sort.index(max_value)
		array_sorted.append(max_value)
		del array_to_sort[max_value_index]
		i += 1

	return array_sorted



def avgList(x):

	n = len(x)

	total = 0

	for element in x:
		total += element

	return float(total)/n


def prodLists(x, y):

	prod_list = []

	if len(x) == len(y):

		i = 0

		while i < len(x):

			product = x[i] * y[i]


			prod_list.append(product)

			i += 1

	else:

		print("Error, the arrays must have the same lenght")



	return prod_list


def squared(x):

	squared_x = []

	for element in x:
		squared_x.append(element**2)


	return squared_x




def slope(x, y):

	numerator = avgList(prodLists(x,y)) - avgList(x) * avgList(y)

	denominator =  avgList(squared(x)) - avgList(x)**2


	slope = numerator/denominator

	return slope


def intercept(x, y):

	numerator = avgList(squared(x)) * avgList(y) - avgList(x) * avgList(prodLists(x,y))

	denominator = avgList(squared(x)) - avgList(x)**2

	intercept = numerator/denominator

	return intercept



def linear_regression(x,y):

	linear_regression = []

	for element in x:

		y_fit = element * slope(x,y) + intercept(x,y)

		linear_regression.append(y_fit)

	return linear_regression



def r_squared(x,y):


	lin_reg = linear_regression(x,y)

	num_difference = []
	den_difference = []

	i = 0

	while i < len(lin_reg):
		num_difference.append(y[i] - lin_reg[i])
		den_difference.append(y[i] - avgList(y))
		i += 1


	num_squared_difference = squared(num_difference)
	den_squared_difference = squared(den_difference)

	total_num_sqd = 0

	total_den_sqd = 0

	for element in num_squared_difference:
		total_num_sqd += element

	for element in den_squared_difference:
		total_den_sqd += element


	r_squared = 0

	numerator = total_num_sqd

	denominator = total_den_sqd

	r_squared = 1 - (numerator/denominator)

	return r_squared


def r(x,y):

	r_sq = r_squared(x,y)

	r = math.sqrt(r_sq)

	return r

def total(x):

	tot = 0

	for element in x:

		tot += element

	return tot



def s(x, y):

	lr = linear_regression(x,y)

	errors = []

	squared_errors = []

	i = 0

	while i < len(lr):

		error = lr[i] - y[i]

		errors.append(error)

		i += 1


	for error in errors:
		error_squared = error ** 2
		squared_errors.append(error_squared)

	numerator = total(squared_errors)

	denominator = len(lr) - 2

	s = math.sqrt(numerator/denominator)

	return s



def sigma(x,y):

        mean = avgList(y)

        errors_from_mean = []
 

        for element in y:
                error_from_mean = element - mean
                errors_from_mean.append(error_from_mean)

                

        errors_from_mean_squared = squared(errors_from_mean)

        numerator = total(errors_from_mean_squared)

        denominator = len(y)

        mse = math.sqrt(numerator/denominator)

        return mse
                


def prevision(x,y):

	prevision = 0

	next_x_element = x[-1] + 1

	prevision = next_x_element * slope(x,y) + intercept(x,y)

	return prevision




