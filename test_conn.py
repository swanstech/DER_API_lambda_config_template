import json
import boto3
import psycopg2
from botocore.exceptions import ClientError


SECRET_NAME = "aws_postgres_swans_database"
REGION_NAME = "ap-southeast-2"


def get_db_secret():
    """Fetch DB credentials from Secrets Manager"""
    client = boto3.client("secretsmanager", region_name=REGION_NAME)

    try:
        response = client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(response["SecretString"])
        return secret
    except ClientError as e:
        print("Failed to retrieve secret:", e)
        raise


def test_db_connection(secret):
    """Test database connection and simple query"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=secret["host"],
            port=secret.get("port", 5432),
            user=secret["user"],
            password=secret["password"],
            dbname=secret["dbname"],
            connect_timeout=5
        )

        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()

        return result[0] == 1

    except Exception as e:
        print("Database connection failed:", e)
        raise

    finally:
        if conn:
            conn.close()


def lambda_handler(event, context):
    try:
        secret = get_db_secret()
        print("Secrets Manager connected successfully")

        db_ok = test_db_connection(secret)
        print("Database connected successfully")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Secrets Manager and Database connection successful",
                "database_test": db_ok
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Connection test failed",
                "error": str(e)
            })
        }
