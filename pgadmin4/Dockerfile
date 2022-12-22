# image=jenek46/pgadmin4:latest
FROM dpage/pgadmin4:6.17
# ENV PGADMIN_DEFAULT_EMAIL=admin@localhost.com
# ENV PGADMIN_DEFAULT_PASSWORD=admin
RUN mkdir -p /var/lib/pgadmin/storage/admin_localhost.com
# COPY --chown=5050:5050 sql/* /var/lib/pgadmin/storage/admin_localhost.com/
COPY --chown=5050:5050 servers.json /pgadmin4/servers.json
COPY --chown=5050:5050 pgpassfile /var/lib/pgadmin/storage/admin_localhost.com/
USER root
RUN chmod 0600 /var/lib/pgadmin/storage/admin_localhost.com/pgpassfile
USER pgadmin