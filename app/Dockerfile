FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install --global serve
COPY --from=builder /app/build ./build
RUN npm install uuid
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]