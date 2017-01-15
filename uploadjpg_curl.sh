curl -X POST \
-H 'Host: www.googleapis.com' \
-H 'Content-Type: image/jpeg' \
-H 'Content-Length: number_of_bytes_in_file' \
-H 'Authorization: Bearer your_auth_token' \
-T sample.jpg \
https://www.googleapis.com/upload/drive/v3/files?uploadType=media
