# DER_API_lambda_config_template
It is to document the DER dashboard Lambda api configuration process


# Structure
The project is consist of a lambda function for the API, an authoriser template, db_seeding SQL file to fill out the database and a token decoder
1. pentest_results_lambda.py: It is using Python 3.12 on AWS, there is only one get API with a required parameter customer_id

   This Lambda function is using a layer for package "psycopg2", please find the layer psycopg2 version 9 in custom layers which suits the Python 3.12
   
2. authoriser_template.py: It is a Python file to be used for the above lambda function authorisation in API Gateway. By using this authoriser we can easily do the role based access control. Please find the comments in the file for using this template.
   
   And for more information about how does the authoriser work, please then refer to the documantation in the team folder
   
3.  db_seeding.py: It is only used for seeding the databsed for the above lambda function, as this api is using mock data for showcase purpose.
4. token_decoder.py: It is a Python file to show how does the token to be decoded in the authoriser.
                      But this authoriser is not using Keyclock JWT decoder for this time, but just the general decoding logic.

# Use case
This repo is used for developers not familiar with AWS serverless API building, providing lambda examples both for api building and authoriers setup.
But the authoriser templated can be used for all later API authorisation by just changing the role required for the new scenario
