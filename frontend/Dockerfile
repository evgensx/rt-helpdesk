# build stage
FROM node:19.4.0-buster as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY ./ .

RUN npm run build


# production stage
FROM nginx:1.23.3 as production-stage

# RUN mkdir /app
# WORKDIR /app

# COPY --from=build-stage /app/dist/ /app
# COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=build-stage /app/dist/ /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]