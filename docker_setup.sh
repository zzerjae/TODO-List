docker run \
    -e DB_HOST="YOUR_DB_HOST_SERVER" \
    -e DB_NAME="YOUR_DB_NAME"\
    -e DB_USER="YOUR_DB_USERNAME" \
    -e DB_PASSWORD="YOUR_DB_PASSWORD" \
    --rm -it \
    -p 8080:80 \
    todolist sh
