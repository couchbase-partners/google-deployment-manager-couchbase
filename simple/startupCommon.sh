echo "Running startupCommon.sh"

function get_metadata_value() {
  curl --retry 5 -s -f \
      -H "Metadata-Flavor: Google" \
      "http://metadata/computeMetadata/v1/$1"
}

function get_attribute_value() {
  get_metadata_value "instance/attributes/$1"
}

readonly ACCESS_TOKEN=$(get_metadata_value "instance/service-accounts/default/token" | awk -F\" '{ print $4 }')
readonly PROJECT_ID=$(get_metadata_value "project/project-id")
readonly EXTERNAL_IP=$(get_metadata_value "instance/network-interfaces/0/access-configs/0/external-ip")

readonly CONFIG=$(get_attribute_value "runtime-config-name")

readonly EXTERNAL_IP_VAR_PATH=$(get_attribute_value "external-ip-variable-path")
readonly SUCCESS_STATUS_PATH="$(get_attribute_value "status-success-base-path")/$(hostname)"
readonly FAILURE_STATUS_PATH="$(get_attribute_value "status-failure-base-path")/$(hostname)"

readonly NODE_PRIVATE_DNS=$(get_metadata_value "instance/hostname")

#######################################################
##### Read external IP and store in runtime-config ####
#######################################################

readonly EXTERNAL_IP_PAYLOAD="$(printf '{"name": "%s", "text": "%s"}' \
  "projects/${PROJECT_ID}/configs/${CONFIG}/variables/${EXTERNAL_IP_VAR_PATH}" \
  "${EXTERNAL_IP}")"

# Updating the value of external-ip variable.
curl -s -k -X PUT \
  -d "${EXTERNAL_IP_PAYLOAD}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-GFE-SSL: yes" \
  https://runtimeconfig.googleapis.com/v1beta1/projects/${PROJECT_ID}/configs/${CONFIG}/variables/${EXTERNAL_IP_VAR_PATH}
