# Chevar AI — istalgan serverda ishlashi uchun
FROM python:3.12-slim
WORKDIR /app
COPY . .
# Ma'lumotlar shu papkada saqlanadi (Volume shu yerga ulanadi)
ENV DATA_DIR=/data
RUN mkdir -p /data
CMD ["python", "-u", "bot.py"]
