FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV SPARK_HOME=/opt/spark
ENV HIVE_HOME=/opt/hive
ENV HIVE_CONF_DIR=/opt/hive/conf
ENV PYSPARK_PYTHON=python3
ENV PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$HIVE_HOME/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-8-jdk \
    python3 \
    python3-pip \
    curl \
    wget \
    tar \
    netcat-openbsd \
    procps \
    ca-certificates \
    && rm -rf /var/lib/apt-get/lists/*

# Download & Install Hadoop 3.3.6
RUN curl -fSL https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -o /tmp/hadoop.tar.gz \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt/ \
    && mv /opt/hadoop-3.3.6 $HADOOP_HOME \
    && rm /tmp/hadoop.tar.gz

# Download & Install Hive 3.1.3
RUN curl -fSL https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz -o /tmp/hive.tar.gz \
    && tar -xzf /tmp/hive.tar.gz -C /opt/ \
    && mv /opt/apache-hive-3.1.3-bin $HIVE_HOME \
    && rm /tmp/hive.tar.gz

# Fix Hive 3.1.3 Guava Conflict (Replace Hive guava-19.0.jar with Hadoop guava-27.0-jre.jar)
RUN rm -f $HIVE_HOME/lib/guava-19.0.jar \
    && cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar $HIVE_HOME/lib/

# Download & Install Spark 3.5.3 (built for Hadoop 3)
RUN curl -fSL https://archive.apache.org/dist/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz -o /tmp/spark.tgz \
    && tar -xzf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-3.5.3-bin-hadoop3 $SPARK_HOME \
    && rm /tmp/spark.tgz

# Install Python packages required for YARN executors, Spark, ML, and Backend
RUN pip3 install --no-cache-dir \
    pyspark==3.5.3 \
    pandas \
    numpy \
    scikit-learn \
    joblib \
    pyarrow \
    fastapi \
    uvicorn \
    pydantic \
    pytest \
    httpx

# Prepare HDFS & volume directories
RUN mkdir -p /hadoop/dfs/name /hadoop/dfs/data /hadoop/tmp /opt/hive/metastore_db /scripts /solar-app

WORKDIR /solar-app

COPY docker/hadoop-base/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
