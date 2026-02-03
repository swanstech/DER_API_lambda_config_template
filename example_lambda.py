import os
import json
import boto3
import psycopg2
import psycopg2.extras

secrets_client = boto3.client("secretsmanager")

def get_db_secret():
    secret_arn = os.environ["DB_SECRET_ARN"]
    resp = secrets_client.get_secret_value(SecretId=secret_arn)
    return json.loads(resp["SecretString"])

def get_connection():
    s = get_db_secret()
    return psycopg2.connect(
        host=s["host"],
        port=int(s.get("port", 5432)),
        dbname=s["dbname"],
        user=s["user"],
        password=s["password"],
        connect_timeout=5,
        sslmode="require",
        cursor_factory=psycopg2.extras.RealDictCursor
    )

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        customer_id = params.get("customer_id")

        if not customer_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "customer_id is required"}, default=str),
            }

        conn = get_connection()
        cur = conn.cursor()

        # 1) All customer_test_results rows for this customer_id
        # (customer_id is only in customer_test_request, so we join via test_id)
        cur.execute(
            """
            SELECT
                r.result_id,
                r.test_id,
                r.asset_id,
                r.risk_id,
                r.recommendation_id,
                r.updated_date
            FROM customer_test_results r
            JOIN customer_test_request req
              ON req.test_id = r.test_id
            WHERE req.customer_id = %s
            ORDER BY r.updated_date DESC
            """,
            (customer_id,),
        )
        results_rows = cur.fetchall()

        # 2) Risk details only for risks referenced by this customer's results
        cur.execute(
            """
            SELECT DISTINCT
                d.risk_id,
                d.risk_probability,
                d.risk_impact,
                d.risk_treatment_options,
                d.updated_date
            FROM customer_test_risk_details d
            JOIN customer_test_results r
              ON r.risk_id = d.risk_id
            JOIN customer_test_request req
              ON req.test_id = r.test_id
            WHERE req.customer_id = %s
            ORDER BY d.updated_date DESC
            """,
            (customer_id,),
        )
        risk_rows = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "customer_id": customer_id,
                    "customer_test_results": results_rows,
                    "customer_test_risk_details": risk_rows,
                },
                default=str,
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {"message": "Failed to fetch data", "error": str(e)},
                default=str,
            ),
        }