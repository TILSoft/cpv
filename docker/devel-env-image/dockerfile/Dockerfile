FROM jupyter/scipy-notebook

USER root

ADD --chown=1000:100 /instantclient_11_2/* /ORACLE/

ENV ORACLE_HOME="/ORACLE"
ENV LD_LIBRARY_PATH=$ORACLE_HOME

RUN apt-get update && \
    apt-get install -y --no-install-recommends libaio-dev libaio1 && \
    rm -rf /var/lib/apt/lists/* && \
    echo "export ORACLE_HOME=/ORACLE" >> /etc/profile && \
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME" >> /etc/profile && \
    echo $LD_LIBRARY_PATH/ >> /etc/ld.so.conf.d/oracle.conf && \
    ln -s $ORACLE_HOME/libclntsh.so.11.1  $ORACLE_HOME/libclntsh.so && \
    ldconfig


#uid=1000(jovyan)
USER $NB_UID

RUN conda install --quiet --yes \
    'cx_Oracle' \
    'pyodbc' \
    'mysql-connector-python'\
    'conda-build' && \
    conda build purge-all && \    
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
