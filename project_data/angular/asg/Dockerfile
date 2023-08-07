FROM node:latest AS build
WORKDIR /usr/src/app
 
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY ["package.json", "package-lock.json", "./"]
 
RUN npm install
RUN npm install -g @angular/cli
RUN npm install --save-dev @angular-devkit/build-angular
COPY . .
 
FROM nginx:1.19.7-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]