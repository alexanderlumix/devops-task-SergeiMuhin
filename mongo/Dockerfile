FROM mongo:7.0.16

# Copy keyfile with correct permissions  
COPY mongo-keyfile /etc/mongo-keyfile
RUN chmod 600 /etc/mongo-keyfile && chown mongodb:mongodb /etc/mongo-keyfile

# Copy startup script
COPY start-mongo.sh /start-mongo.sh
RUN chmod +x /start-mongo.sh

# Copy healthcheck.sh
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh

# Override the entrypoint completely
ENTRYPOINT ["/start-mongo.sh"]