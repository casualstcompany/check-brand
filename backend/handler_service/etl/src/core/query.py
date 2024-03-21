from psycopg2 import sql

BASE_TEMPLATE_EXTRACT_QUERY_SQL = sql.SQL(
    "SELECT {model_list_simple_field_names},"
    "{model_list_complex_fields_meta_array_agg} "
    "{model_meta_greatest} AS updated_at "
    "FROM {model_meta_schema}.{model_meta_table} {model_meta_table}"
    "{model_list_complex_fields_meta_left_join} "
    "WHERE {model_meta_greatest_no_max} > '{last_update_at}' "
    "GROUP BY {model_meta_table}.{model_meta_field_group_by} "
    "ORDER BY {model_meta_greatest} ASC "
)
