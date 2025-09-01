SELECT
  user_pseudo_id,
  event_name,
  (SELECT value.string_value
   FROM UNNEST(event_params)
   WHERE key = "event_label") AS event_label,
  (SELECT 
     CASE 
       WHEN ep.key = 'value' THEN COALESCE(ep.value.int_value, ep.value.float_value)
     END
   FROM UNNEST(event_params) AS ep
   WHERE ep.key = 'value') AS page_duration_value,
  event_timestamp,
  event_date,
  "B" AS version
FROM
  `abtest-versionb.analytics_486567307.events_20250422`

UNION ALL

SELECT
  user_pseudo_id,
  event_name,
  (SELECT value.string_value
   FROM UNNEST(event_params)
   WHERE key = "event_label") AS event_label,
  (SELECT 
     CASE 
       WHEN ep.key = 'value' THEN COALESCE(ep.value.int_value, ep.value.float_value)
     END
   FROM UNNEST(event_params) AS ep
   WHERE ep.key = 'value') AS page_duration_value,
  event_timestamp,
  event_date,
  "B" AS version
FROM
  `abtest-versionb.analytics_486567307.events_20250423`

ORDER BY
  user_pseudo_id,
  event_timestamp;
