#######################################################
##### Notify waiter that machine's setup is done ######
#######################################################

SUCCESS_PAYLOAD="$(printf '{"name": "%s", "text": "%s"}' \
  "projects/${PROJECT_ID}/configs/${CONFIG}/variables/${SUCCESS_STATUS_PATH}" \
  "success")"

echo "Sending success notification for startup waiter"

# Notify waiter
curl -s -k -X POST \
  -d "${SUCCESS_PAYLOAD}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-GFE-SSL: yes" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables
