# gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${APP_ENDPOINT_PORT:-8045} --preload --log-level ${VERBOSIT:-INFO} live.main:app
python main.py