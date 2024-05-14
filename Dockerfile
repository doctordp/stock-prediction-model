FROM python:3.10-bookworm

RUN mkdir -p /home/user/app
RUN mkdir -p /home/user/data
WORKDIR /home/user/app
COPY requirements.txt requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install --upgrade pip \
    # remove this line if necessary PyTorch with CPU+GPU support
    && pip install torch~=2.0.1 torchvision~=0.15.2 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --upgrade -r requirements.txt

RUN wget http://minio-repo.tcl.local:9000/ai-models/torch/sentence_transformers/sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip
RUN unzip sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip
RUN rm -f sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip

RUN python -c 'from transformers import pipeline; pipeline("sentiment-analysis", model="sangrimlee/bert-base-multilingual-cased-nsmc")'

RUN rm -f requirements.txt

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "trace"]