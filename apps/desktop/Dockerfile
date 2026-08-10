FROM node:20-alpine AS builder

WORKDIR /app

COPY packages/widgets ./packages/widgets
COPY apps/desktop/package.json ./apps/desktop/package.json

WORKDIR /app/apps/desktop
RUN npm install --legacy-peer-deps

COPY apps/desktop ./
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app/apps/desktop

ENV NODE_ENV=production
ENV PORT=1420
ENV HOST=0.0.0.0

COPY --from=builder /app/apps/desktop/package.json ./package.json
COPY --from=builder /app/apps/desktop/.next ./.next
COPY --from=builder /app/apps/desktop/node_modules ./node_modules
COPY --from=builder /app/apps/desktop/public ./public

EXPOSE 1420

CMD ["npm", "start"]
