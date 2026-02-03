-- =========================================
-- Mock data seed for SWANS_DATABASE (PostgreSQL)
-- Tables:
--   customer (already has 2 rows)
--   customer_test_request
--   customer_test_results
--   customer_test_risk_details

-- =========================================




BEGIN;

-- -----------------------------
-- 1) CLEAN (reverse dependency)
-- -----------------------------

TRUNCATE TABLE
  customer_test_results,
  customer_test_risk_details,
RESTART IDENTITY;



  
-- -----------------------------------------
-- 1) INSERT customer_test_results
--    (ties test_id -> risk_id)
-- -----------------------------------------
INSERT INTO customer_test_results (
  result_id,
  test_id,
  asset_id,
  risk_id,
  recommendation_id,
  updated_date
)
VALUES
  ('RES_10',  'T_61', 'AT_61', 'RISK_10', 'RECOMM_10', '2026-02-01 12:10:00.000'::timestamp),
  ('RES_10B', 'T_61', 'AT_61', 'RISK_11', 'RECOMM_11', '2026-02-01 12:15:00.000'::timestamp),
  ('RES_11',  'T_62', 'AT_62', 'RISK_11', 'RECOMM_11', '2026-02-02 11:10:00.000'::timestamp),
  ('RES_12',  'T_63', 'AT_63', 'RISK_12', 'RECOMM_12', '2026-01-31 10:10:00.000'::timestamp),
  ('RES_13',  'T_64', 'AT_64', 'RISK_13', 'RECOMM_13', '2026-02-03 09:10:00.000'::timestamp);
 
 

 
-- -----------------------------------------
-- 2) INSERT customer_test_risk_details
--    (risk_impact varchar(10), treatment varchar(100))
-- -----------------------------------------
INSERT INTO customer_test_risk_details (
  risk_id,
  risk_probability,
  risk_impact,
  risk_treatment_options,
  updated_date
)
VALUES
  ('RISK_10', 3, 'HIGH',   'Validate JWT iss/aud, short TTL, rotate keys', '2026-02-01 12:00:00.000'::timestamp),
  ('RISK_11', 2, 'MEDIUM', 'Least-privilege IAM, scope ARNs, rotate secrets', '2026-02-02 11:00:00.000'::timestamp),
  ('RISK_12', 4, 'HIGH',   'Harden DB grants, enable audit logs, rotate creds', '2026-01-31 10:00:00.000'::timestamp),
  ('RISK_13', 3, 'MEDIUM', 'Enforce roles server-side, deny-by-default logging', '2026-02-03 09:00:00.000'::timestamp);
