# GmId_Streamlit_LookUpTables
The application is user-friendly and allows for comprehensive data processing, management, and analysis with a clear and organized user interface.

# How to use it?
The first step is to obtain the look up tables. In my particular case I do use Cadence Virtuoso for this purpose.
What we need to do is to do a sweep of four variables VGS, VDS, VSB and L. After that we need to save the following outputs gm, gds, cgs, ID, vgs, vov.
! The only limitation is that when doing the sweep we need to do it in this order:


# Execute the code
What we need to do is to run the main.py from the terminal with the following command:
streamlit run main.py

Since the streamlit code has been uploaded in GitHub the website can also be run online, however, the ability to save files is not made for this purpose, and for that reason is recommended to clone the repository and use it locally.

We will see that on the webpage that opens in locally we can access different pages:

![image](https://github.com/user-attachments/assets/52e2128a-89d9-46e1-9754-4dc56e13af57)
Initially, we won't have any data, the reason for which we won't be able to do any plot. Therefore, the first step is to upload the data.

# Import the data and create the look-up tables:
From the Load RAW data, we can set upload and choose our csv file, once its updated we will be able to see a preview of the database and select the ranges of values with which we have worked. Those values correspond to the Cadence sweep range that we defined during the simulation. Take into consideration that we won't be able to see these options until we haven't uploaded a file.
![image](https://github.com/user-attachments/assets/df3ae614-3e31-4904-b6e5-0a3efd8d45d4)


