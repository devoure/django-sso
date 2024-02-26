version: '3'
volumes:
  postgres_data:
      driver: local
services:
  dater:
      build:
          context: ../dater-app/.
      container_name: dater
      command: python dater/manage.py runserver 0.0.0.0:8000
      ports:
          - 8000:8000
      volumes:
          - ../dater-app/dater:/app/dater
      depends_on:
          - keycloak
  hello:
      build:
          context: ../hello-app/.
      container_name: hello
      command: python hello/manage.py runserver 0.0.0.0:8001
      ports:
          - 8001:8001
      volumes:
          - ../hello-app/hello:/app/hello
      depends_on:
          - keycloak

  postgres:
      image: postgres
      volumes:
        - postgres_data:/var/lib/postgresql/data
      environment:
        POSTGRES_DB: keycloak
        POSTGRES_USER: keycloak
        POSTGRES_PASSWORD: password
  keycloak:
      image: quay.io/keycloak/keycloak:legacy
      environment:
        DB_VENDOR: POSTGRES
        DB_ADDR: postgres
        DB_DATABASE: keycloak
        DB_USER: keycloak
        DB_SCHEMA: public
        DB_PASSWORD: password
        KEYCLOAK_USER: admin
        KEYCLOAK_PASSWORD: admin
        # Uncomment the line below if you want to specify JDBC parameters. The parameter below is just an example, and it shouldn't be used in production without knowledge. It is highly recommended that you read the PostgreSQL JDBC driver documentation in order to use it.
        #JDBC_PARAMS: "ssl=true"
      ports:
        - 8080:8080
      depends_on:
        - postgres
