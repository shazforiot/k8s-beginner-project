# ─────────────────────────────────────────────
# Stage 1: Build dependencies
# ─────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ─────────────────────────────────────────────
# Stage 2: Runtime image
# ─────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# 1. Copy packages to a location appuser can actually read
# Instead of /root/.local, we'll put them in the standard site-packages
COPY --from=builder /root/.local/lib/python3.12/site-packages /home/appuser/.local/lib/python3.12/site-packages
COPY --from=builder /root/.local/bin /home/appuser/.local/bin

# 2. Setup the user first
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# 3. Update PATH to point to the new user-accessible location
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/home/appuser/.local/lib/python3.12/site-packages

COPY app.py .

EXPOSE 8080

# Health check at Docker level (complements K8s probes)
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

CMD ["python", "app.py"]
