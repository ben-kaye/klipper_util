import numpy as np
import os.path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f = open(__location__ + "\\printer.cfg", "r")

array = []

# parse printer.cfg

in_auto_gen = False
in_points = False

for line in f:
    if in_auto_gen:
        if in_points:
            if "=" in line:
                in_points = False
                in_auto_gen = False
                break
            else:
                array.append(line)

        if "points" in line and "=" in line:
            in_points = True

    if "bed_mesh" in line and "#*#" in line:
        in_auto_gen = True

f.close()

# format values

grid = []
for grid_line in array:
    points = grid_line.split(' ')[-5:]
    formatted_points = [float(x.replace(',', '').replace(
        '\t', '').replace('\n', '')) for x in points]
    grid.append(formatted_points)



# flatten list
z = []
for u in grid:
    z.extend(u)


# make A and b in Ax=b
g = list(range(1, len(grid)+1))

x = g*len(grid)
y = [k for k in range(1, len(grid)+1) for _ in range(1, len(grid)+1)]
ones = [1 for u in range(1, len(grid)**2 + 1)]

A = np.array([x, y, ones], dtype='float32').transpose()

z = np.array(z).reshape(len(grid)**2, 1)

# solve
coeffs = np.linalg.lstsq(A, z)[0]

z_new = [None]*len(x)

# compute new plane
for i in range(len(x)):
    new_val = float(coeffs[0]*x[i] + coeffs[1]*y[i] + coeffs[2])

    z_new[i] = "{:.4f}".format(new_val)


# reformat values
lines = []
for i in range(len(grid)):

    s = ', '

    x = z_new[len(grid)*i:len(grid)*(i+1)]

    line_text = '#*# \t ' + s.join(x) + '\n'
    lines.append(line_text)

#print
f = open(__location__ + '\\config_out.txt', 'w')
for l in lines:
    f.write(l)
f.close()
