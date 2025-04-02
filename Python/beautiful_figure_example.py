"""
This example demonstrates how to create a beautiful figure using the the Matplotlib library.

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
    'font.size': 12,
    'axes.titlesize': 12,
    'axes.labelsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 12
})

# # Creating a not very beautiful plot with default parameters:
fig, ax = plt.subplots(figsize=(10, 10)) # <-- the resulting PNG figure will be 640×480 pixels by default
ax.set_xlabel(f"{feature_names[x_col].capitalize()}")
ax.set_ylabel(f"{feature_names[y_col].capitalize()}")


# plt.axis('equal')  # Keep aspect ratio equal
# plt.gca().set_aspect('equal', adjustable='box')  # Maintain square shape


# Major grid:
ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.25)

# Minor ticks and grid:
ax.minorticks_on()
ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.25)

ax.set_axisbelow(True) # <-- Ensure grid is below data


# #  https://www.color-hex.com/color-palette/106106 <-- This is an interesting colour palette that we will use as a basis
# # Let's define colours for the datasets ['setosa', 'versicolor', 'virginica']:
dataset_colors = ['#9671bd', '#7e7e7e', '#77b5b6'] 
dataset_line_colors = ['#6a408d', '#4e4e4e', '#378d94']

# # Plotting in a loop for each dataset:
for class_name in datasets_to_plot:
    class_index = list(target_names).index(class_name)  # Get correct label
    class_mask = y_target == class_index
    data_x = X_data[class_mask, x_col].reshape(-1, 1)
    data_y = X_data[class_mask, y_col]

    # Scatter plot:
    ax.scatter(data_x, data_y, 
               label = class_name.capitalize(),
               s = 50,
               color = dataset_colors[class_index],
               edgecolors = dataset_line_colors[class_index],
               linewidths = 1.5
    )

    # Linear regression:
    lin_model = LinearRegression().fit(data_x, data_y)
    x_range = np.linspace(data_x.min() - 1.0, data_x.max() + 1.0, 100).reshape(-1, 1)
    y_pred_linear = lin_model.predict(x_range)
    ax.plot(x_range, y_pred_linear, label=f"{class_name.capitalize()} LR")

    # Polynomial regression:
    poly = PolynomialFeatures(polynomial_degree)
    data_x_poly = poly.fit_transform(data_x)
    poly_model = LinearRegression().fit(data_x_poly, data_y)
    x_range_poly = poly.transform(x_range)
    y_pred_poly = poly_model.predict(x_range_poly)
    ax.plot(x_range, y_pred_poly, label=f"{class_name.capitalize()} PR (degree {polynomial_degree})")

ax.legend() # adding the legend



# # Save and show the figure:
plt.savefig("beautiful_figure_python.png", dpi=100) # <-- saving as PNG (raster graphic) is not ideal for publications
plt.savefig("beautiful_figure_python.pdf") # <-- vector-based image, great for publications and further editing
plt.savefig("beautiful_figure_python.svg") # <-- vector-based image, great for publications and further editing

plt.show()
