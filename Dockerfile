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

RUN wget --header="Host: drive.usercontent.google.com" --header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" --header="Accept-Language: en-GB,en-US;q=0.9,en;q=0.8" --header="Cookie: NID=514=TCfT6XLf30fICzhnTWfM2-PjCUb1RG5Qw9WUFddE9dGnYMPGsRHsyvmzTycF1CzVaP30U5vwLPgAd6fuu5c4oQWtGCsvXyZef3tg82z-cLRhqX5dtRyA1zOB55n6Pr80MwPa3cWJpSDwCUVM7gvnR2ic7zjT5pVTawHdcIU7IlI" --header="Connection: keep-alive" "https://drive.usercontent.google.com/download?id=1DQjFHjT-1aKfUWY-iDHBFYVAaNKMzQND&export=download&confirm=t&uuid=4a3cac59-3a3c-4bb4-afc6-41385fa6ffec" -c -O 'sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip'
RUN unzip sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip
RUN rm -f sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2.zip

RUN python -c 'from transformers import pipeline; pipeline("sentiment-analysis", model="sangrimlee/bert-base-multilingual-cased-nsmc")'

RUN rm -f requirements.txt

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "trace"]