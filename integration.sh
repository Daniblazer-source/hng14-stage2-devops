#!/bin/bash
set -e

echo "🚀 Starting Integration Tests..."

# 1. Check Frontend
echo "Checking Frontend..."
curl -f http://localhost:3000 || (echo "Frontend Down"; exit 1)

# 2. Submit a Job via the Proxy
echo "Submitting Job..."
RESPONSE=$(curl -s -X POST http://localhost:3000/submit)
JOB_ID=$(echo $RESPONSE | jq -r '.job_id // empty')

if [ -z "$JOB_ID" ] || [ "$JOB_ID" == "null" ]; then
    echo "❌ Failed to get Job ID. Response: $RESPONSE"
    exit 1
fi

echo "✅ Created Job: $JOB_ID"

# 3. Check Status (Polling)
echo "Checking Status..."
for i in {1..5}; do
    STATUS=$(curl -s http://localhost:3000/status/$JOB_ID | jq -r '.status')
    echo "Current Status: $STATUS"
    if [ "$STATUS" == "completed" ] || [ "$STATUS" == "queued" ]; then
        echo "🎉 Integration Test Passed!"
        exit 0
    fi
    sleep 2
done

echo "❌ Integration Test Timed Out"
exit 1
