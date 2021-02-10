docker run \
--name aurora-app \
--mount type=bind,source="$(pwd)"/src,target=/code \
-p 8080:80 \
-d \
aurora-app