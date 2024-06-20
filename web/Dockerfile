# TODO: rewrite with multi stage

FROM node:22-alpine

ARG $PORT

ENV NEXT_TELEMETRY_DISABLED 1

WORKDIR /app
RUN corepack enable

COPY .yarnrc.yml \
    env.d.ts \
    next.config.mjs \
    tsconfig.json \
    ./

COPY package.json yarn.lock ./
RUN yarn set version berry
RUN yarn install --immutable

COPY public ./public
COPY src ./src

EXPOSE $PORT

CMD yarn dev
