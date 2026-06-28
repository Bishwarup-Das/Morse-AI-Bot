# Use the official uv image with Python 3.10 (matches .python-version)
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Avoid Python writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Compile bytecode for faster startup and copy mode for caching
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first (cached layer) using the lockfile
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the application source
COPY bot.py ./

# Sync again to install the project itself
RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Run as a non-root user for security
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Make sure the virtualenv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Start the bot
CMD ["python", "bot.py"]
