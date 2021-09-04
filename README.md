# capstoneproject-comp9900-w16a-excellent
## Installation Guide

System requirement:  

- Lubuntu  20.4.1 LTS 
- Python 3.7.10 z513 
- pip 21.1.2   
- Git  

 

To deploy this project, users must first obtain the source files from GitHub to local: 

- SSH:  

  Git clone [git@github.com:COMP3900-9900-Capstone-Project/capstoneproject-comp9900-w16a-excellent.git ](mailto:git@github.com:COMP3900-9900-Capstone-Project/capstoneproject-comp9900-w16a-excellent.git ) 

- HTTP:  

  Git clone https://github.com/COMP3900-9900-Capstone-Project/capstoneproject-comp9900-w16a-excellent.git  



**NOTE:** Testing environment is a virtual machine based on the Lubuntu 20.4.1 LTS virtual machine image here: https://rebrand.ly/o1fy80n 



Then follow the steps to deploy the project on the server.  

After downloading our repo to your local host, you can find a compressed version of our running file called value_eats.zip. 

1. Uncompressed the files:	```unzip value_eats.zip ```	and make sure following items are included in the directory: 


- admin.py
- index.py
- login.py
- mysession.py
- vouhcer.py
- config.json
- service_account.json

2. Install required python packages by running:  

   ```pip install –r requirement.txt ```

3. Run the program 

   ```python index.py```

4. Now open your browser and visit:     ```localhost:8881```

    For admin user, you need to visit: 	```localhost:8881/admin```
 

Alternatively, if you wish to build the project from the source code and run it, you could: 

1. Install node.js 

2. Enter the “front-end” folder, run:

   ```npm install``` 

3. In the front-end folder, run:

   ```npm run build```

   After building, a “dist” folder will be generated in current folder. 

4. Move the “dist” folder to a new folder named “value_eats” 

5. Move the python code admin.py, index.py, login.py and voucher.py from backend folder to “value_eats”  folder (the same folder in step 4)

6. Move config.json file from backend folder to value_eats 

7. Move service_account.json and requirement.txt to value_eats 

8. Install required python packages by running:  

   ```pip install –r requirements.txt ```

9. Run the program 

   ```python index.py ```

10. Now open your browser and visit: 

    ```localhost:8881 ```

Since admin account is not allowed to create through the web page, here is one offered for admin testing.

​		Email:	excellenteatery@outlook.com

​		Password:	123456 

If you have any issue when building and running the program, please feel free to contact any member from the group. 
