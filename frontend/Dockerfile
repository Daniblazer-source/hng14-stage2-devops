# Stage 1: Build dependencies
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package*.json ./
RUN npm install --production

# Stage 2: Final runtime image
FROM node:18-alpine

WORKDIR /app

# Create a non-root user for security (Alpine specific)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy dependencies and source code
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Secure the application files
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

# HEALTHCHECK: Verify the Express server is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["node", "app.js"]
