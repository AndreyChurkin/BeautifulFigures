"""
This example demonstrates a basic figure generated with the Matplotlib library:
- All plotting parameters are left at their defaults, with no customisation of fonts, colours, or layout
- The figure is saved in PNG file format (raster graphic)

Such a default plotting can lead to several issues when preparing figures for a manuscript:
- The figure size may be arbitrary, and the aspect ratio may not suit the layout of a paper.
- The image resolution (in pixels) may be too low, causing problems when exporting or resizing.
- Since saved in PNG, the figure will have pixels and lack the sharpness of vector graphics.
- The default font may not be ideal for a scientific publication.
- Also, the font might be small, which creates readability/visibility problems in the manuscript.
- The weights of lines may be inadequate. For example, some lines may be overly thin or thick.
- Similarly, the size of markers may be inconsistent.
- The default colours may not work well for our data. We may need to select another colour scheme.
- The legend may be misplaced, overlapping with data or taking excessive space outside the figure canvas.

To avoid these problems, we fine-tune the plotting parameters in 'beautiful_figure_example.py'

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



# # Creating a not very beautiful plot with default parameters:
fig, ax = plt.subplots() # <-- the resulting PNG figure will be 640×480 pixels by default
ax.set_xlabel(f"{feature_names[x_col].capitalize()}")
ax.set_ylabel(f"{feature_names[y_col].capitalize()}")



# # Plotting in a loop for each dataset:
for class_name in datasets_to_plot:
    class_index = list(target_names).index(class_name)  # Get correct label
    class_mask = y_target == class_index
    data_x = X_data[class_mask, x_col].reshape(-1, 1)
    data_y = X_data[class_mask, y_col]

    # Scatter plot:
    ax.scatter(data_x, data_y, label=class_name.capitalize())

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
plt.savefig("not_a_very_beautiful_figure_python.png") # <-- saving as PNG (raster graphic) is not ideal for publications
# plt.savefig("not_a_very_beautiful_figure_python.pdf") # <-- vector-based image, great for publications and further editing
# plt.savefig("not_a_very_beautiful_figure_python.svg") # <-- vector-based image, great for publications and further editing

plt.show()
