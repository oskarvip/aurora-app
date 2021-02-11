echo "Removing current aurora-app"
docker stop aurora-app
docker rm aurora-app
echo "Starting up the aurora-app"
docker run \
--name aurora-app \
--mount type=bind,source="$(pwd)"/src,target=/code \
--env-file "$(pwd)"/.env \
-p 8080:80 \
-d \
aurora-app