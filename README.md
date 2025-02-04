# GmId Streamlit Lookup Tables
The app is user-friendly and makes it easy to handle and analyze data with a clear and organized interface. Traditional hand calculations use basic transistor models like the quadratic one, but these models don't consider second-order effects. This can cause the results to differ quite a bit from what you expect. It usually takes several tries to get the final result. The Gm/Id methodology aims to simplify the design process by using Lookup Tables (LUTs) instead of MOSFET models. Each of the lookup tables defines a parameter, which is affected by the bias, geometry, and second-order effects that are modeled by the simulator.
Setting up these tables is required just once for a specific technology, the goal of this GitHub is the generation of such tables and the modes of operation of analysis. It is out of the scope of this project to explain how this will be used in a design, books on the Gm/Id methodology should be used. 

## Table of Contents
- [How to use it](#how-to-use-it)
- [Execute the code](#execute-the-code)
- [Import the data and create the look-up tables](#import-the-data-and-create-the-look-up-tables-load-raw-data)
- [Plot](#plot)
- [Get value](#get-value)
- [Ratio](#ratio)
- [Create your own graph](#create-your-own-graph)
- [Cross Lookup](#cross-lookup)
- [References and Guidelines](#references-and-guidelines)

## How to use it?
The first step is to obtain the lookup tables. In my particular case, I do use Cadence Virtuoso for this purpose. We need to sweep four variables VGS, VDS, VSB, and L. After that, we need to save the following outputs gm, gds, cgs, ID, vgs, vov.
<strong style="color:red;">!</strong>
 The only limitation is that when doing the sweep we need to do it in this order:
![image](https://github.com/user-attachments/assets/65add828-ce04-4ac8-83fa-ee865d4954e4)
![image](https://github.com/user-attachments/assets/bb28bef6-44fe-451a-ad3d-12df5f83bfad)

Once the simulation has finished we need to go to Plot - Main Plot. On the window that opens we need to:
![image](https://github.com/user-attachments/assets/96ce9f13-247a-4ba9-90b7-50e64b82a0d2)

and select the psf file. From there a Brower window will open on the left, we must select the dcOpInfo and export the data in a table. Once in the table, we can export it in any format of our convenience

![image](https://github.com/user-attachments/assets/8697ee4f-a0d8-46c6-bd30-ba1fe03c27fa)

<strong style="color:red;">!</strong> One may question why the width of the transistor hasn't been considered as a sweep variable, instead a fixed value of 1 um has been used. Since the majority of analog CMOS circuits take advantage of wide transistors, proportionality holds as far as W is concerned. [1]([https://ieeexplore.ieee.org/document/10122491/])
## Execute the code
What we need to do is to run the main.py from the terminal with the following command:
streamlit run main.py

Since the streamlit code has been uploaded to GitHub the website can also be run online, however, the ability to save files is not made for this purpose, and for that reason is recommended to clone the repository and use it locally.

We will see that on the webpage that opens locally we can access different pages:

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
As an engineer seeing a graph helps us to visualize the tendency of the relationship between three variables, however, to obtain precise calculations we would need to obtain specific values for an x-y pair. For that reason this section allows the designer to specify the parameters and obtain an output.

![image](https://github.com/user-attachments/assets/1fc60eac-5529-4e8d-b0c4-362aa0ba8c4e)

## Ratio
A second type of parameter consists of ratios between the parameters presented before. Some examples would be the drain current density J_D = ID/W, the intrinsic low-frequency gain of the common-source transistor gm/gds, the transit frequency gm/Cgg, and the transconductance efficiency gm/ID. Here we can also see that since both parameters depend on the width any of these ratios are width-independent.
![image](https://github.com/user-attachments/assets/d6e446d8-2b84-4447-9ccf-05e9e1921054)
![image](https://github.com/user-attachments/assets/be48e34b-1b2e-42fd-83d5-1c8a05f696b9)


## Create your graph
The goal of this page is to enable the creation of any graph that the designer requires, beyond the limited options provided by the rest of the design. Additionally, it allows for overlapping multiple graphs, as illustrated in the following example extracted from [1]. This functionality enables more efficient and flexible design processes.
![image](https://github.com/user-attachments/assets/4280c985-d814-4110-8eb2-a711703c20d4)

## Cross Lookup
Finally, the third mode is to have a plot between ratios, an example would be GM_ID and JD.
![image](https://github.com/user-attachments/assets/ce26cd1a-90ae-4ef5-aea3-d7ac2fd975d6)

## Other functionalities
On the sidebar, there are multiple sections. You can select the tables you want to work with. For a proper design, you should include at least both PMOS and NMOS transistors. However, depending on the technology, multiple kinds of transistors may exist (e.g., low noise, low Vt, etc.). Additionally, you can navigate between different pages. If you are visualizing data on a plot, you have the option to save that data to a file and later import it in the "Create Your Graph" page.

![image](https://github.com/user-attachments/assets/ca46c571-a78c-4a51-a283-2e09a40ff7d1)


## References and Guidelines
To further enhance your knowledge and application of the Gm/Id methodology, it is highly recommended to consult the book Systematic Design of Analog CMOS Circuits: Using Pre-Computed Lookup Tables. Additionally, Dr. Hesham's course on the Gm/Id methodology offers valuable insights and practical applications.
