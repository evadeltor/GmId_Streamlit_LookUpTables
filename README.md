# GmId Streamlit Lookup Tables
The app is user-friendly and makes it easy to handle and analyze data with a clear and organized interface. Traditional hand calculations use basic transistor models like the quadratic one, but these models don't consider second-order effects. This can cause the results to differ quite a bit from what you expect. It usually takes several tries to get the final result. The Gm/Id methodology aims to simplify the design process by using Lookup Tables (LUTs) instead of MOSFET models. 

## Table of Contents
- [How to use it](#how-to-use-it)
- [Execute the code](#execute-the-code)
- [Import the data and create the look-up tables](#import-the-data-and-create-the-look-up-tables-load-raw-data)
- [Plot](#plot)
- [Get value](#get-value)
- [Ratio](#ratio)
- [Create your own graph](#create-your-own-graph)
- [Cross Lookup](#cross-lookup)
- [Contributing](#contributing)
- [License](#license)

## How to use it?
The first step is to obtain the look-up tables. In my particular case, I do use Cadence Virtuoso for this purpose. We need to sweep four variables VGS, VDS, VSB, and L. After that, we need to save the following outputs gm, gds, cgs, ID, vgs, vov.
! The only limitation is that when doing the sweep we need to do it in this order:
![image](https://github.com/user-attachments/assets/65add828-ce04-4ac8-83fa-ee865d4954e4)
![image](https://github.com/user-attachments/assets/bb28bef6-44fe-451a-ad3d-12df5f83bfad)


## Execute the code
What we need to do is to run the main.py from the terminal with the following command:
streamlit run main.py

Since the streamlit code has been uploaded in GitHub the website can also be run online, however, the ability to save files is not made for this purpose, and for that reason is recommended to clone the repository and use it locally.

We will see that on the webpage that opens in locally we can access different pages:

![image](https://github.com/user-attachments/assets/52e2128a-89d9-46e1-9754-4dc56e13af57)

Initially, we won't have any data, the reason for which we won't be able to do any plot. Therefore, the first step is to upload the data.

## Import the data and create the look-up tables (Load RAW data):
From the Load RAW data, we can set upload and choose our CSV file, once it is updated we will be able to see a preview of the database and select the ranges of values with which we have worked. Those values correspond to the Cadence sweep range that we defined during the simulation. Take into consideration that we won't be able to see these options until we have uploaded a file.

![image](https://github.com/user-attachments/assets/59e52644-3b4b-49ac-a1df-ea15e9a0e1da)

## Plot
After the processing of the data we are now ready to view the data. Let's start with the plot page. The goal of this first page is to be able to observe the behavior of our transistor considering 2D, the x-axis and a parametric sweep. The functionality is divided in the following sections:
- Variables to select
- Graph properties

![image](https://github.com/user-attachments/assets/2e6e5770-655c-484d-9e2e-77529ee4e54c)

## Get value
Not always is required to see a graph but to 

![image](https://github.com/user-attachments/assets/1fc60eac-5529-4e8d-b0c4-362aa0ba8c4e)

## Ratio
![image](https://github.com/user-attachments/assets/d6e446d8-2b84-4447-9ccf-05e9e1921054)
![image](https://github.com/user-attachments/assets/be48e34b-1b2e-42fd-83d5-1c8a05f696b9)


## Create your own graph

![image](https://github.com/user-attachments/assets/4280c985-d814-4110-8eb2-a711703c20d4)

## Cross Lookup

![image](https://github.com/user-attachments/assets/ce26cd1a-90ae-4ef5-aea3-d7ac2fd975d6)


