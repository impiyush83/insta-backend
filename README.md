# INSTA-BACKEND SERVICE
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/747141aacd1f44e1b6f7d64a8c80452f)](https://www.codacy.com/manual/impiyush83/insta-backend?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=impiyush83/insta-backend&amp;utm_campaign=Badge_Grade)

This is backend as a service built to implement instagram like service where one can follow other users, share photos, like photos and comment on photos.   


-----

# Approach
### Flow 1. Get feed of your connections
- Each user has its own `redis list` having its 10 recent posts.
- Whenever, a user wants to access his feed he hits api which collects all the posts of his followees from redis and sends a response.

### Flow 2. Image Storage
- We use `Depot Storage with S3` for storage of images. 
- Only the link of the image is stored onto database.

----
# Deployment
- Currently, this is not deployed. 

----

# API:

- The link for API documentation : https://documenter.getpostman.com/view/4946631/SW132JDJ?version=latest

----

# Test cases

- Unit Test cases have been added for each module to check the functionality at the grass root level.

----

# Run on your machine 

- Ensure you have installed python3.6 or above and postgres9.x and above. 
- Install dependancies. 

    ```
    pip install -r requirements.txt
    ```
    
- Create database in postgres with user and password

- Change the SQLALCHEMY_DATABASE_URI in the config 

    ```
    postgresql://<username>:<password>@localhost:<post:5432>/<database_name>
    ```
    
- Upgrade the database 

    ```
    python manage.py db upgrade
    ```
    
- Export AWS_SECRET_KEY and AWS_ACCESS_KEY as environment variables

   ```
   export AWS_ACCESS_KEY=<your-key>
   export AWS_SECRET_KEY=<your-key>
   ```
   
- Create bucket in AWS 

- Change depot.bucket value in 
  
  ```
  'depot.bucket': '<bucket_name>'
  ```
  
- Start server
    
    ```
    python manage.py runserver
    ```

# Important commands:

1. To run tests .

    ```
    pytest tests -W ignore::DeprecationWarning
       
    ```
   
