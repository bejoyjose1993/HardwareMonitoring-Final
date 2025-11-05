# Build Angular app
FROM node:22-alpine AS build

ARG BASE_API_URL
ARG FAST_BASE_API_URL
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .

# Inject BASE_API_URL into environment file (optional approach below)
RUN echo "export const environment = { production: true, apiUrl: '${BASE_API_URL}', fpApiUrl: '${FAST_BASE_API_URL}'};" > src/environments/environment.prod.ts

RUN echo "FAST_BASE_API_URL=${FAST_BASE_API_URL}" && echo "BASE_API_URL=${BASE_API_URL}"

RUN npx ng build --configuration production --no-progress

# Serve with Nginx
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/edge_monitor_dashboard/browser /usr/share/nginx/html

# EXPOSE 80
EXPOSE 4200
CMD ["nginx", "-g", "daemon off;"]