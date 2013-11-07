# Input: a list of lists of tuples, which represents one character
# Output: the character in MNIST format

import copy, math

MNIST_LEN = 36

def string_to_tuples(str):
	l = []
	coords = str.split(',')
	for coord in coords:
		x, y = coord.split()
		l.append((float(x), float(y)))
	return l

def display(pixels):
	for row in pixels:
		row_str = ''
		for point in row:
			if point != 0:
				row_str += unichr(0x2588)
			else:
				row_str += ' '
		print row_str

def inkml_to_pixels(inkml_character):
	# Create a copy, and then within each stroke, sort by x and then y value
	inkml_character_copy = copy.deepcopy(inkml_character)
	# for i in range(len(inkml_character_copy)):
	# 	inkml_character_copy[i] = sorted(inkml_character_copy[i])

	# print inkml_character_copy

	# Find the height and width of the character (will be later resized)
	min_x = float('+inf')
	max_x = float('-inf')
	min_y = float('+inf')
	max_y = float('-inf')
	for stroke in inkml_character_copy:
		for x,y in stroke:
			if x < min_x: min_x = x
			if x > max_x: max_x = x
			if y < min_y: min_y = y
			if y > max_y: max_y = y
	width = max_x - min_x
	height = max_y - min_y
	# print 'max y', max_y
	resize_factor = 1.0

	# Figure out the resize factor to fit in a 28 x 28 format
	max_dimension = max(width, height)
	resize_factor = float(MNIST_LEN) / float(max_dimension)
	# print 'width', width, 'height', height, 'max_dimension', max_dimension
	# print 'resize factor', resize_factor

	# Now color the 28 x 28 pixels as 0 or 1
	pixels = []
	for i in range(MNIST_LEN):
		pixels.append([0] * MNIST_LEN)

	for stroke in inkml_character_copy:
		previous_tuple = None
		for x,y in stroke:
			pixel_x = int((x - min_x) * resize_factor)
			pixel_y = int((y - min_y) * resize_factor)
			# print 'x index', pixel_x
			# print 'y index', pixel_y, 'resized from', y, 'with min_y', min_y
			if pixel_y >= MNIST_LEN: pixel_y -= 1
			if pixel_x >= MNIST_LEN: pixel_x -= 1
			pixels[pixel_y][pixel_x] = 1.0  # TODO: See if changes increase accuracy
			if previous_tuple is not None:
				if pixel_x > previous_tuple[0]:
					starting_x = previous_tuple[0]
					ending_x = pixel_x
					starting_y = previous_tuple[1]
					ending_y = pixel_y
				else:
					starting_x = pixel_x
					ending_x = previous_tuple[0]
					starting_y = pixel_y
					ending_y = previous_tuple[1]
				print 'starting x', starting_x, 'ending x', ending_x, 'starting y', starting_y, 'ending y', ending_y
				if ending_x == starting_x:
					for i in range(0, int(math.fabs(ending_y - starting_y))):
						y_index = min(starting_y, ending_y) + i
						x_index = starting_x
						pixels[y_index][x_index] = 1.0
				elif ending_y == starting_y:
					for i in range(0, int(math.fabs(ending_x - starting_x))):
						y_index = starting_y
						x_index = min(starting_x, ending_x) + i
						pixels[y_index][x_index] = 1.0
				else:
					slope = float(ending_y - starting_y) / float(ending_x - starting_x)
					print 'slope', slope
					if slope >= 1.0: # Every y value should have a point
						for i in range(0, ending_y - starting_y):
							y_index = starting_y + i
							x_index = int(starting_x + float(i) / slope)
							# print 'x index', x_index
							# print 'y index', y_index
							pixels[y_index][x_index] = 1.0
					elif slope < 1.0 and slope > 0:  # Every x value should have a point
						for i in range(0, ending_x - starting_x):
							x_index = starting_x + i
							y_index = int(starting_y + float(i) * slope)
							# print 'x index', x_index
							# print 'y index', y_index
							pixels[y_index][x_index] = 1.0
					elif slope < 0 and slope >= -1.0:  # Every x value should have a point
						for i in range(0, ending_x - starting_x):
							y_index = int(starting_y + float(i) * slope)
							x_index = starting_x + i
							pixels[y_index][x_index] = 1.0
					elif slope < -1.0:  # Every y value should have a point
						for i in range(0, starting_y - ending_y):
							y_index = ending_y + i
							x_index = int(ending_x + float(i) / slope)
							pixels[y_index][x_index] = 1.0
			previous_tuple = (pixel_x, pixel_y)
	display(pixels)
	return pixels

l = string_to_tuples("10.2238 21.8766, 10.2198 21.8846, 10.1877 21.9046, 10.1396 21.9408, 10.0714 21.9729, 10.0072 21.9929, 9.955 22.0009, 9.93494 21.9929, 9.9229 21.9729, 9.92691 21.9367, 9.94296 21.8926, 9.97907 21.8525, 10.0192 21.8204, 10.0352 21.8204, 10.0553 21.8404, 10.0714 21.8846, 10.0794 21.9408, 10.0994 21.9969, 10.1075 22.0371, 10.1315 22.0732, 10.1516 22.0852, 10.1837 22.0812, 10.2078 22.0772, 10.2278 22.0571, 10.264 22.0371, 10.284 22.013, 10.3001 21.9809, 10.3121 21.9488, 10.3041 21.9207, 10.292 21.9046, 10.272 21.8926, 10.2559 21.8926, 10.2439 21.8966, 10.2319 21.9046")
# l = string_to_tuples("9.4735 21.3028, 9.49356 21.3268, 9.49356 21.3349, 9.49356 21.3549, 9.48955 21.391, 9.48554 21.4392, 9.48152 21.4914, 9.47751 21.5315, 9.4735 21.5435, 9.47751 21.5435, 9.48152 21.5315, 9.48554 21.4954, 9.49757 21.4352, 9.52165 21.379, 9.5698 21.3268, 9.62196 21.2787, 9.65807 21.2626, 9.68616 21.2667, 9.70221 21.2947, 9.71425 21.3589, 9.70221 21.4312, 9.68215 21.4873, 9.6661 21.5275, 9.65807 21.5315, 9.66209 21.5235, 9.6661 21.4954, 9.69017 21.4432, 9.72227 21.391, 9.75839 21.3589, 9.80252 21.3389, 9.83061 21.3429, 9.84666 21.363, 9.87475 21.4111, 9.87876 21.4552, 9.86271 21.4914, 9.86271 21.5194, 9.8587 21.5475, 9.85067 21.5556")
# l = string_to_tuples("10.6211 21.2787, 10.6451 21.2667, 10.6732 21.2546, 10.7013 21.2426, 10.7174 21.2426, 10.7374 21.2586, 10.7374 21.2988, 10.7134 21.3549, 10.6732 21.4111, 10.613 21.4552, 10.5488 21.4793, 10.4967 21.4673, 10.4686 21.4432, 10.4646 21.4071, 10.4887 21.3509, 10.5248 21.2988, 10.5649 21.2626, 10.601 21.2426, 10.6371 21.2426, 10.6692 21.2586, 10.6732 21.2947, 10.6813 21.3589, 10.6772 21.4472, 10.6853 21.5275, 10.7013 21.6117, 10.7254 21.6639, 10.7495 21.7241, 10.7575 21.7682, 10.7455 21.8003, 10.7134 21.8164, 10.6692 21.8164, 10.609 21.7883, 10.5769 21.7401, 10.5769 21.7, 10.597 21.6599, 10.6171 21.6358, 10.6612 21.6198, 10.7013 21.6157")
# l = string_to_tuples("9.00404 21.5997, 9.02009 21.6037, 9.04416 21.6037, 9.07225 21.5957, 9.13244 21.5756, 9.19263 21.5395, 9.25281 21.4673, 9.28892 21.391, 9.30899 21.3188, 9.30899 21.2626, 9.30497 21.2346, 9.30096 21.2346, 9.29695 21.2466, 9.28892 21.2988, 9.26886 21.4071, 9.25682 21.5515, 9.24078 21.684, 9.23275 21.7843, 9.22071 21.8485, 9.21269 21.8886, 9.20867 21.8966, 9.20466 21.9006, 9.20065 21.8926, 9.20065 21.8806, 9.20065 21.8485, 9.21269 21.7923, 9.23676 21.696, 9.26084 21.5756, 9.28892 21.4793, 9.32102 21.4031, 9.35714 21.3549, 9.38121 21.3389, 9.39325 21.3469, 9.38924 21.371, 9.3772 21.4272, 9.37319 21.4954, 9.36917 21.5475, 9.3772 21.5796, 9.39726 21.5917, 9.41732 21.5877, 9.45745 21.5877, 9.49757 21.5636, 9.53369 21.5435")
# l = string_to_tuples("11.0905 21.0099, 11.0945 21.0018, 11.0905 20.9978, 11.0825 20.9938, 11.0624 20.9858, 11.0143 20.9778, 10.9381 20.9778, 10.8578 20.9778, 10.7816 20.9898, 10.7093 20.9898, 10.6572 20.9938, 10.6171 20.9938, 10.589 20.9978, 10.5649 21.0018, 10.5368 20.9978, 10.5127 21.0018, 10.5007 21.0179, 10.4927 21.0139, 10.4887 21.0139, 10.4846 21.0179, 10.4766 21.0219, 10.4646 21.0219, 10.4566 21.0219, 10.4566 21.0179, 10.4606 21.0219, 10.4646 21.0219, 10.4686 21.0219, 10.4726 21.0219, 10.4766 21.0179, 10.4927 21.0219, 10.5127 21.0339, 10.5488 21.062, 10.601 21.1021, 10.6652 21.1503, 10.7254 21.1864, 10.7615 21.2105, 10.7936 21.2305, 10.8016 21.2386, 10.7976 21.2386, 10.8016 21.2426, 10.7976 21.2426, 10.7936 21.2426, 10.7856 21.2506, 10.7695 21.2586, 10.7374 21.2747, 10.6853 21.3188, 10.6211 21.363, 10.5729 21.3991, 10.5368 21.4352, 10.4927 21.4593, 10.4566 21.4793, 10.4365 21.4954, 10.4245 21.5034, 10.4245 21.5074, 10.4285 21.5074, 10.4365 21.5074, 10.4525 21.5074, 10.4766 21.5074, 10.5127 21.5154, 10.5769 21.5275, 10.6813 21.5435, 10.7936 21.5435, 10.91 21.5435, 11.0143 21.5556, 11.0825 21.5596, 11.1106 21.5636, 11.1146 21.5676, 11.1106 21.5716, 11.0945 21.5756")
inkml_to_pixels([l])

