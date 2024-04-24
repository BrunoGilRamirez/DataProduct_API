# syntax=docker/dockerfile:1


ARG PYTHON_VERSION=3.11.8
FROM python:${PYTHON_VERSION}-alpine as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1 
WORKDIR /app


#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser
#give permission read, write and execute to the appuser in the /app directory
#RUN chown -R appuser /app
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
#this --mount=type=cache,target=/root/.cache/pip is used to cache the pip packages, if you don't use it, the pip packages will be downloaded every time you build the image
#RUN --mount=type=cache,target=/root/.cache/pip \ 
#    --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    python -m pip install -r requirements.txt


# Switch to the non-privileged user to run the application.
#USER appuser

# Copy the source code into the container.
COPY . .
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8000

CMD uvicorn main:wdm --host 0.0.0.0 --port 8000   