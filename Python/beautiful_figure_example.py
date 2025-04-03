"""
This example demonstrates how to create a beautiful figure using the Matplotlib library.

Multiple plotting parameters are fine-tuned to produce a clean, publication-ready figure:
- We adjust the figure size and the X/Y axis ranges.
- We set the font style and size for readability.
- We modify the layout by adjusting plot margins, adding a frame, and setting an equal aspect ratio.
- We control grid lines and axis ticks.
- We select a harmonious, minimalistic colour scheme for all markers and lines.
- We adjust the line widths and the size of the markers.

Finally, we export the figure in PDF and SVG formats (vector-based graphics), which will allow us to use it in a manuscript without loss of quality.

Andrey Churkin https://andreychurkin.ru/

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import load_iris

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)



# # Load the Iris flower dataset:
iris_data = load_iris()

# # Get data and target:
X_data = iris_data.data  # Features (sepal length, sepal width, petal length, petal width)
y_target = iris_data.target  # Target (species: 0=setosa, 1=versicolor, 2=virginica)

# # Get feature names and target names:
feature_names = iris_data.feature_names
target_names = iris_data.target_names



# # Choose feature columns to plot, for example: Sepal length (0) vs Sepal width (1)
x_col = 0;  y_col = 1
# x_col = 2;  y_col = 3

# # Select the degree of a polynomial regression:
polynomial_degree = 2
# polynomial_degree = 3
# polynomial_degree = 4

# # Select the datasets to visualise:
# datasets_to_plot = target_names # <-- all datasets
# datasets_to_plot = ['setosa']
# datasets_to_plot = ['virginica']
# datasets_to_plot = ['setosa', 'versicolor', 'virginica'] # <-- all datasets
datasets_to_plot = ['setosa', 'virginica']



# # Defining the fonts before plotting:
plt.rcParams.update({
    'font.family': 'Courier New',  # or try 'monospace' if you’re unsure it's installed
    'font.size': 20,
    'axes.titlesize': 20,
    'axes.labelsize': 20,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'legend.fontsize': 20,
    'figure.titlesize': 20
}) 
# Note: when placed in a 0.9*column_width space in a IEEE journal template, 20pt will be displayed as 8pt, which matches the font size of the figure description text

# # Creating a plot and then adjusting multiple parameters to make it beautiful:
fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlabel(f"{feature_names[x_col].capitalize()}")
ax.set_ylabel(f"{feature_names[y_col].capitalize()}")


ax.set_aspect('equal', adjustable='datalim') # Lock the square shape


# Major grid:
ax.grid(True, which='major', linestyle='-', linewidth=0.75, alpha=0.25)

# Minor ticks and grid:
ax.minorticks_on()
ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)

ax.set_axisbelow(True) # <-- Ensure grid is below data



# # Now let's work on the colours:

# # https://www.color-hex.com/color-palette/106106 <-- This is an interesting colour palette that we will use as a basis
# # Let's define colours for the datasets ['setosa', 'versicolor', 'virginica']:
dataset_colors = ['#9671bd', '#7e7e7e', '#77b5b6'] 
dataset_line_colors = ['#6a408d', '#4e4e4e', '#378d94']

# # And the colour for the lines (regressions):
regression_color = '#8a8a8a' # <-- neutral grey
# regression_color = '#7f9fa1' # <-- greyish seafoam



# # Plotting in a loop for each dataset:
all_data_x_to_plot = [] 
all_data_y_to_plot = []
regression_flag = 0 # control plotting of regression labels
for class_name in datasets_to_plot:
    class_index = list(target_names).index(class_name)  # Get correct label
    class_mask = y_target == class_index
    data_x = X_data[class_mask, x_col].reshape(-1, 1)
    data_y = X_data[class_mask, y_col]

    # Scatter plot:
    ax.scatter(data_x, data_y, 
               label = class_name.capitalize(),
               s = 90,
               color = dataset_colors[class_index],
               edgecolors = dataset_line_colors[class_index],
               linewidths = 1.5,
               zorder = 3
    )

    # Linear regression:
    lin_model = LinearRegression().fit(data_x, data_y)
    x_range = np.linspace(data_x.min() - 10.0, data_x.max() + 10.0, 100).reshape(-1, 1)
    y_pred_linear = lin_model.predict(x_range)
    ax.plot(x_range, y_pred_linear, 
            label="LR" if regression_flag == 0 else "_nolegend_",
            linewidth = 2.6,
            color = regression_color,
            zorder = 2 # use the z-order to force scatter to be displayed over lines
    )

    # Polynomial regression:
    poly = PolynomialFeatures(polynomial_degree)
    data_x_poly = poly.fit_transform(data_x)
    poly_model = LinearRegression().fit(data_x_poly, data_y)
    x_range_poly = poly.transform(x_range)
    y_pred_poly = poly_model.predict(x_range_poly)
    ax.plot(x_range, y_pred_poly, 
            label="PR" if regression_flag == 0 else "_nolegend_",
            linewidth = 2.6,
            color = regression_color,
            linestyle = '--',
            zorder = 2
    )

    # Tracking which data we plot to adjust plotting limits later:
    all_data_x_to_plot.extend(data_x)
    all_data_y_to_plot.extend(data_y)

    regression_flag += 1
    


# # Setting the legend:
handles, labels = ax.get_legend_handles_labels() # get all legend items
desired_order = [0, 3, 1, 2]  # change the order of legend elements

ax.legend(
    [handles[i] for i in desired_order],
    [labels[i] for i in desired_order],
    loc = 'upper center',
    bbox_to_anchor = (0.5, 1.10),  # center top, above axes
    ncol = 4,                      # spread horizontally
    frameon = False                # removes legend border
) 



# # Define how much to zoom out from the data plotting range (cm):
# zoom_out = 0.5
zoom_out = 0.6
# zoom_out = 1.0

x_min = min(all_data_x_to_plot)
x_max = max(all_data_x_to_plot)
x_median = (x_min + x_max)/2
x_range = x_max - x_min

y_min = min(all_data_y_to_plot)
y_max = max(all_data_y_to_plot)
y_median = (y_min + y_max)/2
y_range = y_max - y_min

plotting_range = max([x_range, y_range]) + zoom_out

# # Set the new plotting limits explicitly
ax.set_xlim(x_median - plotting_range/2, x_median + plotting_range/2)
ax.set_ylim(y_median - plotting_range/2, y_median + plotting_range/2)



# # Save and show the figure:
# plt.tight_layout() # <-- automatically adjust spacing between subplots and elements
""" Warning: tight_layout() can make the plotting area not square (setting an arbitrary size) """

plt.savefig("beautiful_figure_python.png", dpi=100) # <-- saving as PNG (raster graphic) is not ideal for publications
plt.savefig("beautiful_figure_python.pdf") # <-- vector-based image, great for publications and further editing
plt.savefig("beautiful_figure_python.svg") # <-- vector-based image, great for publications and further editing

plt.show()
