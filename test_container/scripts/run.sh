/opt/spark/bin/spark-submit --master local[*] --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:/home/sparkpy/conf/log4j.properties" --conf "spark.executor.extraJavaOptions=-Dlog4j.configuration=file:/home/sparkpy/conf/log4j.properties" /home/sparkpy/main.py "devapp" "{\"max_file_age\": \"2d\"}" "$(cat topics/topics.json)"