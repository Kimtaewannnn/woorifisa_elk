db_tables =  [
"df_brazil",
"df_euro",
"df_ftse",
"df_gold",
"df_india",
# "df_kor10y",
# "df_kor3y",
"df_kospi",
"df_nasdaq",
"df_nikkei",
# "df_usa10y",
# "df_usa3y",
"df_taiwan"  
]


# db table -> for문을 통해, 양옆 공백 제거
arr = []
for i in db_tables:
    arr.append(i.strip())

#print(arr)

print("input {")
# jdbc -> plugin db table 복사 완료.
for i in range(0,len(arr)):
    print("    jdbc {")
    print("        clean_run => true")
    print("        jdbc_driver_library => \"/usr/share/logstash/logstash-core/lib/jars/mysql-connector-java-8.0.30.jar\"")
    print("        jdbc_driver_class => \"com.mysql.jdbc.Driver\"")
    print("        jdbc_connection_string =>  \"jdbc:mysql://team5-db.cvqn3ewwzknb.ap-northeast-2.rds.amazonaws.com:3306/symbol\"")
    print("        jdbc_user => \"admin\"")
    print("        jdbc_password => \"woorifisa\"")
    print("        jdbc_paging_enabled => true")
    print("        tracking_column => \"unix_ts_in_secs\"")
    print("        use_column_value => true")
    print("        tracking_column_type => \"numeric\"")
    print("        schedule => \"*/5 * * * * *\"")
    print(f"       statement => \"SELECT *, UNIX_TIMESTAMP(Date) AS unix_ts_in_secs FROM {arr[i]} WHERE (UNIX_TIMESTAMP(Date) > :sql_last_value) ORDER BY Date ASC\"")
    print("        last_run_metadata_path => \"/usr/share/logstash/.logstash_jdbc_last_run\"")
    print(f"        type => \"{arr[i]}\"")
    print("        }")
    print("\n")
print("}")

print("filter {")
print("   date {")
print("        match => [\"Date\", \"YYYY-MM-dd HH:mm:ss\"]")
print("        target => \"@timestamp\"")
print("        timezone => \"Asia/Seoul\"")
print("        locale => \"ko\"")
print("    }")

print("  mutate {")
print("    copy => {\"Date\" => \"[@metadata][Date]\"}")
print("    remove_field => [\"Date\", \"@version\",  \"unix_ts_in_secs\"]")
print("    }")
print("  }")

print("output {")
# for 문 if 조건
for i in range(0,len(arr)):
    print(f"    if[type] == \"{arr[i]}\""  "  {")
    print("        elasticsearch {")
    print("            hosts => \"elasticsearch:9200\"")
    print(f"           index => \"logstash-{arr[i].split('_')[1]}\"")
    print("            user => \"logstash_internal\"")
    print("            password => \"${LOGSTASH_INTERNAL_PASSWORD}\"")
    # print("            document_id => \"%{[@metadata][Date]}\"")
    print("            }")
    print("    }")

print("    stdout {")
print("        codec => rubydebug")
print("    }")
print("}")