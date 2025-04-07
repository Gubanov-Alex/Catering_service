FROM python:3.12-slim

#ENV PYTHONUNBUFFERED=1

WORKDIR /app/


RUN apt-get update -y \
    # dependencies for building Python packages && cleaning apt apt packages
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --upgrade pip setuptools pipenv \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools pipenv watchdog

COPY archiv/Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

# copy the project
COPY ./ ./

EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]