docker run -d \
  --name middle-where \
  -e TEST_ENV=f00 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  middle-where
