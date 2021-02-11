echo "Removing current aurora_app"
docker stop aurora_app
docker rm aurora_app
echo "Starting up the aurora_app"
docker run \
--name aurora_app \
--mount type=bind,source="$(pwd)"/src,target=/code \
--env-file "$(pwd)"/.env \
-p 8080:80 \
-d \
aurora_app