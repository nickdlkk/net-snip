FROM python:3.11.0-buster as builder

WORKDIR /usr/src/wheels

RUN pip install -U \
    pip \
    setuptools \
    wheel

COPY requirements.txt ./
RUN pip install wheel && pip wheel -r requirements.txt

FROM python:3.11.0-slim-buster

LABEL authors="Nick"
ENV TINI_VERSION="v0.19.0"

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN groupadd -g 61000 app && useradd -g 61000 -l -M -s /bin/false -u 61000 app

WORKDIR /usr/src/app

# 复制构建阶段生成的wheel包
COPY --from=builder /usr/src/wheels /usr/src/wheels
COPY requirements.txt ./

RUN pip install -r requirements.txt -f ./ \
    && rm -rf /usr/src/wheels \
    && rm -rf /root/.cache/pip/*

# 复制应用源代码
COPY . /usr/src/app

EXPOSE 5000

USER app
ENTRYPOINT ["/tini", "--"]
CMD ["python", "index.py"]