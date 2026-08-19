FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY suites ./suites
COPY fixtures ./fixtures
RUN pip install --no-cache-dir .
ENTRYPOINT ["studio-test-runner"]
CMD ["--help"]
