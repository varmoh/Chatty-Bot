FROM python:3.9

WORKDIR /app

COPY Chatty-Bot/ .

COPY helpers/ .

RUN python /app/helpers/install_modules.py

# Expose any ports if needed
# EXPOSE 5000
# EXPOSE 5001

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
