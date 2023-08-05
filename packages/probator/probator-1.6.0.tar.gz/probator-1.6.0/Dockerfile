# vim: set ft=Dockerfile:
FROM python:3.7-alpine

ARG pip_flags
ARG extra_packages
ARG timezone=UTC

ENV PATH="/probator/bin:${PATH}"
ENV TZ=$timezone

# Install dependencies
RUN apk --no-cache add libffi-dev gcc make libc-dev mariadb-dev git tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo "UTC" > /etc/timezone

# Add Probator user and install the virtual environment
RUN adduser -Dh /home/probator probator
RUN mkdir -p /var/log/probator /probator
RUN chown probator:probator /var/log/probator /probator

# Switch to the probator user and install the packages
USER probator
RUN python3.7 -m venv /probator
RUN /probator/bin/pip install --no-cache-dir -U $pip_flags \
    probator-auditor-cloudtrail probator-auditor-domain-hijacking probator-auditor-iam probator-auditor-required-tags \
    probator-auditor-vpc-flowlogs probator-collector-dns probator-scheduler-sqs $extra_packages pip

WORKDIR /probator
EXPOSE 5000
CMD ["probator", "shell"]
