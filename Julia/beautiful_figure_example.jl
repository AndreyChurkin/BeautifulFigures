"""
This example demonstrates how to create a beautiful figure using the Julia Plots.jl package.
- Multiple plotting parameters are fine-tuned to produce a clean, publication-ready figure:
- We adjust the figure size and the X/Y axis ranges.
- We set the font style and size for readability.
- We modify the layout by adjusting plot margins, adding a frame, and setting an equal aspect ratio.
- We control grid lines and axis ticks.
- We select a harmonious, minimalistic colour scheme for all markers and lines.
- We adjust the line widths and the size of the markers.

Finally, we export the figure in PDF and SVG formats (vector-based graphics), which will allow us to use it in a manuscript without loss of quality.

Andrey Churkin https://andreychurkin.ru/

"""

using Plots, Plots.PlotMeasures
using StatsPlots

cd(dirname(@__FILE__))
println(pwd())



# # The "Iris" dataset: sepal length, sepal width, petal length, petal width

SetosaData = [
5.1	3.5	1.4	0.2
4.9	3.0	1.4	0.2
4.7	3.2	1.3	0.2
4.6	3.1	1.5	0.2
5.0	3.6	1.4	0.2
5.4	3.9	1.7	0.4
4.6	3.4	1.4	0.3
5.0	3.4	1.5	0.2
4.4	2.9	1.4	0.2
4.9	3.1	1.5	0.1
5.4	3.7	1.5	0.2
4.8	3.4	1.6	0.2
4.8	3.0	1.4	0.1
4.3	3.0	1.1	0.1
5.8	4.0	1.2	0.2
5.7	4.4	1.5	0.4
5.4	3.9	1.3	0.4
5.1	3.5	1.4	0.3
5.7	3.8	1.7	0.3
5.1	3.8	1.5	0.3
5.4	3.4	1.7	0.2
5.1	3.7	1.5	0.4
4.6	3.6	1.0	0.2
5.1	3.3	1.7	0.5
4.8	3.4	1.9	0.2
5.0	3.0	1.6	0.2
5.0	3.4	1.6	0.4
5.2	3.5	1.5	0.2
5.2	3.4	1.4	0.2
4.7	3.2	1.6	0.2
4.8	3.1	1.6	0.2
5.4	3.4	1.5	0.4
5.2	4.1	1.5	0.1
5.5	4.2	1.4	0.2
4.9	3.1	1.5	0.1
5.0	3.2	1.2	0.2
5.5	3.5	1.3	0.2
4.9	3.1	1.5	0.1
4.4	3.0	1.3	0.2
5.1	3.4	1.5	0.2
5.0	3.5	1.3	0.3
4.5	2.3	1.3	0.3
4.4	3.2	1.3	0.2
5.0	3.5	1.6	0.6
5.1	3.8	1.9	0.4
4.8	3.0	1.4	0.3
5.1	3.8	1.6	0.2
4.6	3.2	1.4	0.2
5.3	3.7	1.5	0.2
5.0	3.3	1.4	0.2]

VersicolorData = [
7.0	3.2	4.7	1.4
6.4	3.2	4.5	1.5
6.9	3.1	4.9	1.5
5.5	2.3	4.0	1.3
6.5	2.8	4.6	1.5
5.7	2.8	4.5	1.3
6.3	3.3	4.7	1.6
4.9	2.4	3.3	1.0
6.6	2.9	4.6	1.3
5.2	2.7	3.9	1.4
5.0	2.0	3.5	1.0
5.9	3.0	4.2	1.5
6.0	2.2	4.0	1.0
6.1	2.9	4.7	1.4
5.6	2.9	3.6	1.3
6.7	3.1	4.4	1.4
5.6	3.0	4.5	1.5
5.8	2.7	4.1	1.0
6.2	2.2	4.5	1.5
5.6	2.5	3.9	1.1
5.9	3.2	4.8	1.8
6.1	2.8	4.0	1.3
6.3	2.5	4.9	1.5
6.1	2.8	4.7	1.2
6.4	2.9	4.3	1.3
6.6	3.0	4.4	1.4
6.8	2.8	4.8	1.4
6.7	3.0	5.0	1.7
6.0	2.9	4.5	1.5
5.7	2.6	3.5	1.0
5.5	2.4	3.8	1.1
5.5	2.4	3.7	1.0
5.8	2.7	3.9	1.2
6.0	2.7	5.1	1.6
5.4	3.0	4.5	1.5
6.0	3.4	4.5	1.6
6.7	3.1	4.7	1.5
6.3	2.3	4.4	1.3
5.6	3.0	4.1	1.3
5.5	2.5	4.0	1.3
5.5	2.6	4.4	1.2
6.1	3.0	4.6	1.4
5.8	2.6	4.0	1.2
5.0	2.3	3.3	1.0
5.6	2.7	4.2	1.3
5.7	3.0	4.2	1.2
5.7	2.9	4.2	1.3
6.2	2.9	4.3	1.3
5.1	2.5	3.0	1.1
5.7	2.8	4.1	1.3]

VirginicaData = [
6.3	3.3	6.0	2.5
5.8	2.7	5.1	1.9
7.1	3.0	5.9	2.1
6.3	2.9	5.6	1.8
6.5	3.0	5.8	2.2
7.6	3.0	6.6	2.1
4.9	2.5	4.5	1.7
7.3	2.9	6.3	1.8
6.7	2.5	5.8	1.8
7.2	3.6	6.1	2.5
6.5	3.2	5.1	2.0
6.4	2.7	5.3	1.9
6.8	3.0	5.5	2.1
5.7	2.5	5.0	2.0
5.8	2.8	5.1	2.4
6.4	3.2	5.3	2.3
6.5	3.0	5.5	1.8
7.7	3.8	6.7	2.2
7.7	2.6	6.9	2.3
6.0	2.2	5.0	1.5
6.9	3.2	5.7	2.3
5.6	2.8	4.9	2.0
7.7	2.8	6.7	2.0
6.3	2.7	4.9	1.8
6.7	3.3	5.7	2.1
7.2	3.2	6.0	1.8
6.2	2.8	4.8	1.8
6.1	3.0	4.9	1.8
6.4	2.8	5.6	2.1
7.2	3.0	5.8	1.6
7.4	2.8	6.1	1.9
7.9	3.8	6.4	2.0
6.4	2.8	5.6	2.2
6.3	2.8	5.1	1.5
6.1	2.6	5.6	1.4
7.7	3.0	6.1	2.3
6.3	3.4	5.6	2.4
6.4	3.1	5.5	1.8
6.0	3.0	4.8	1.8
6.9	3.1	5.4	2.1
6.7	3.1	5.6	2.4
6.9	3.1	5.1	2.3
5.8	2.7	5.1	1.9
6.8	3.2	5.9	2.3
6.7	3.3	5.7	2.5
6.7	3.0	5.2	2.3
6.3	2.5	5.0	1.9
6.5	3.0	5.2	2.0
6.2	3.4	5.4	2.3
5.9	3.0	5.1	1.8
]



# # Select which columns to analyse:
columns_to_plot = "sepal_length_vs_sepal_width"
# columns_to_plot = "petal_length_vs_petal_width"

if columns_to_plot == "sepal_length_vs_sepal_width"
    global plot_x_label = "Sepal length, cm"
    global plot_y_label = "Sepal width, cm"
    global data_x_column = 1
    global data_y_column = 2
elseif columns_to_plot == "petal_length_vs_petal_width"
    global plot_x_label = "Petal length, cm"
    global plot_y_label = "Petal width, cm"
    global data_x_column = 3
    global data_y_column = 4
end



# # Select the degree of a polynomial regression:
polynomial_degree = 2
# polynomial_degree = 3
# polynomial_degree = 4



# # Defining additional functions for performing regressions:

function my_linear_regression(Data, X_predict)
    # # linear regression:
    X = Data[:, 1]  # Predictor (first column)
    y = Data[:, 2]  # Response (second column)
    X_design = [ones(length(X)) X]  # Add a column of ones for the intercept
    β = X_design \ y  # Solves (X'X)β = X'y
    X_predict_design = [ones(length(X_predict)) X_predict]
    Y_predict = X_predict_design * β
    return Y_predict
end

function my_polynomial_regression(Data, X_predict, degree)
    X = Data[:, 1]  # Predictor (first column)
    y = Data[:, 2]  # Response (second column)
    if degree == 2
        # # Quadratic polynomial regression:
        X_design = [ones(length(X)) X X.^2]
        β = X_design \ y 
        X_predict_design = [ones(length(X_predict)) X_predict X_predict.^2]
        Y_predict = X_predict_design * β
    elseif degree == 3
        # # Cubic regression:
        X_design = [ones(length(X)) X X.^2 X.^3]
        β = X_design \ y 
        X_predict_design = [ones(length(X_predict)) X_predict X_predict.^2 X_predict.^3]
        Y_predict = X_predict_design * β
    elseif degree == 4
        # # Polynomial regressionof degree 4:
        X_design = [ones(length(X)) X X.^2 X.^3 X.^4]
        β = X_design \ y 
        X_predict_design = [ones(length(X_predict)) X_predict X_predict.^2 X_predict.^3 X_predict.^4]
        Y_predict = X_predict_design * β
    end
    return Y_predict
end



# # Select the datasets to visualise:
# datasets_to_plot = ["Iris setosa"]
# datasets_to_plot = ["Iris setosa", "Iris versicolor", "Iris virginica"]
datasets_to_plot = ["Iris setosa", "Iris virginica"]



# Creating a combined dataset for tuning plotting parameters later:
global combined_datasets_to_plot = Array{Float64}(undef, 0, 4)
for check_dataset = 1:size(datasets_to_plot)[1]
    dataset_name = datasets_to_plot[check_dataset]
    if dataset_name == "Iris setosa"
        add_Data = deepcopy(SetosaData) 
    elseif dataset_name == "Iris versicolor"
        add_Data = deepcopy(VersicolorData) 
    elseif dataset_name == "Iris virginica"
        add_Data = deepcopy(VirginicaData) 
    end
    global combined_datasets_to_plot = vcat(combined_datasets_to_plot,add_Data)
end



# # Let's create a beautiful figure by tuning multiple plotting parameters!


# # Set the font size for elements of the figure:
# fz = 14 # fontsize <-- too small
fz = 18 # fontsize <-- great for IEEE journal templates


# # Define how much to zoom out from the data plotting range (cm):
# zoom_out = 0.5
zoom_out = 0.6
# zoom_out = 1.0


x_min = minimum(combined_datasets_to_plot[:,data_x_column])
x_max = maximum(combined_datasets_to_plot[:,data_x_column])
x_median = (x_min + x_max)/2
x_range = x_max - x_min

y_min = minimum(combined_datasets_to_plot[:,data_y_column])
y_max = maximum(combined_datasets_to_plot[:,data_y_column])
y_median = (y_min + y_max)/2
y_range = y_max - y_min

plotting_range = maximum([x_range, y_range]) + zoom_out


# # Creating the plot (canvas), setting general plotting parameters:
beautiful_plot = plot(
    xlabel = plot_x_label,
    ylabel = plot_y_label,

    size = (1000,1000), # <-- width and height of the whole plot (in px)

    xlim = (x_median - plotting_range/2, x_median + plotting_range/2),
    ylim = (y_median - plotting_range/2, y_median + plotting_range/2), 
    aspect_ratio = :equal,

    xtickfontsize = fz, ytickfontsize = fz,
    fontfamily = "Courier", 
    titlefontsize = fz,
    xguidefontsize = fz,
    yguidefontsize = fz,
    legendfontsize = fz-6,

    # legend = :false,
    legend = :true,


    framestyle = :box,
    margin = 10mm,
    
    # grid = :false,
    grid = :true,

    # minorgrid = :false,
    minorgrid = :true,

    # minorTicks = true,

    xticks = 0:0.5:10, # to ensure that we have correct minor ticks
    yticks = 0:0.5:10
)

# #  https://www.color-hex.com/color-palette/106106 <-- This is an interesting colour palette that we will use as a basis

# # Plotting in a loop for each dataset:
regression_flag = 0 # control plotting of regression labels
for vis_dataset = 1:size(datasets_to_plot)[1]
    dataset_name = datasets_to_plot[vis_dataset]

    if dataset_name == "Iris setosa"
        Data0 = deepcopy(SetosaData)
        # dataset_color = palette(:tab10)[5]
        dataset_color = "#9671bd"
        dataset_linecolor = "#6a408d"
    elseif dataset_name == "Iris versicolor"
        Data0 = deepcopy(VersicolorData) 
        dataset_color = palette(:tab10)[8]
    elseif dataset_name == "Iris virginica"
        Data0 = deepcopy(VirginicaData) 
        # dataset_color = palette(:tab10)[10]
        dataset_color = "#77b5b6"
        dataset_linecolor = "#378d94"
    end

    global Data1 = Data0[:,[data_x_column,data_y_column]]

    # # Define the range for regression:
    X_range = range(0, 10, length=100) 
    # X_range = range(minimum(Data0[:,1])-1, maximum(Data0[:,1])+1, length=100)

    plot!(beautiful_plot,
        X_range,
        my_linear_regression(Data1, X_range),
        # label = "LR",
        label = regression_flag == 0 ? "LR" : false,
        # color = palette(:tab10)[8], # grey from the default palette
        color = RGB(0.3, 0.3, 0.3), # grey defined manually via RGB components
        w = 4
    )

    plot!(beautiful_plot,
        X_range,
        my_polynomial_regression(Data1, X_range, polynomial_degree),
        # label = "PR",
        label = regression_flag == 0 ? "PR" : false,
        # color = palette(:tab10)[8], # grey from the default palette
        color = RGB(0.3, 0.3, 0.3), # grey defined manually via RGB components
        w = 4,
        linestyle = :dash
    )

    scatter!(beautiful_plot,
        Data1[1:end,data_x_column], Data1[1:end,data_y_column], 
        label = dataset_name,
        markersize = 8,
        markerstrokewidth = 1.5,
        color = dataset_color,

        # color = RGB(184/255, 204/255, 234/255) # PANTONE 2708 C #b8ccea
        # color = RGB(204/255, 234/255, 184/255) # CCEAB8

        markerstrokecolor = dataset_linecolor
    )

    global regression_flag += 1
end


display(beautiful_plot)

# # Exporting the figure:
figure_name = "beautiful_figure_example"
savefig(figure_name*".png") # <-- saving as PNG is not ideal for publications
savefig(figure_name*".svg") # <-- vector-based image, great for publications and further editing
savefig(figure_name*".pdf") # <-- vector-based image, great for publications and further editing
