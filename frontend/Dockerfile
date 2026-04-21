# Stage 1: builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --production

# Stage 2: Final
FROM node:18-alpine
WORKDIR /app

# Create named non-root user for Frontend
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

RUN chown -R appuser:appgroup /app
USER appuser

# FIX: Set environment variable to ensure Node listens on all interfaces
ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

# FIX: Use a simpler healthcheck or increase start-period to allow the app to boot
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["node", "app.js"]
