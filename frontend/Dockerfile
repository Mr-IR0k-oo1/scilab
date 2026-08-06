FROM oven/bun:1.1-slim AS builder

WORKDIR /app

# Copy package files
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy application source
COPY . .

# Build production assets
RUN bun run build

FROM oven/bun:1.1-slim AS runner

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/src/index.ts ./src/index.ts
COPY --from=builder /app/src/index.html ./src/index.html

EXPOSE 3000

ENV NODE_ENV=production

CMD ["bun", "src/index.ts"]
