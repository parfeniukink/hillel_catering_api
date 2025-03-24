# /bin/bash
# actually in the cicd file is fine

cd ~/projects/hillel_catering_api

git pull
docker compose build && docker compose down && docker compose up -d

echo "🚀 Successfully deployed"

