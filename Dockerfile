FROM jupyter/scipy-notebook:latest

USER root

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER jovyan

# Instalar pacotes Python
RUN pip install --no-cache-dir \
    great-expectations==0.18.8 \
    sqlalchemy==1.4.46 \
    pandas \
    numpy \
    matplotlib \
    seaborn

# Configurar diretório de trabalho
WORKDIR /home/jovyan/work

# Expor porta do Jupyter
EXPOSE 8888

# Comando padrão
CMD ["start-notebook.sh", "--NotebookApp.token='dataops123'"]