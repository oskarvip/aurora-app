echo "Removing current aurora_app"
docker stop aurora_app
docker rm aurora_app
echo "Starting up the aurora_app"
docker run \
--name aurora_app \
--mount type=bind,source="$(pwd)"/src,target=/code \
-e MAPBOX_ACCESS_TOKEN \
-p 8080:8080 \
-d \
aurora_app
