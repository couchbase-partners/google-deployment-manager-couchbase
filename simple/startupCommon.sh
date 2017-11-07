echo "Running startupCommon.sh"

function get_metadata_value() {
  curl --retry 5 -s -f \
      -H "Metadata-Flavor: Google" \
      "http://metadata/computeMetadata/v1beta1/$1"
}

function get_attribute_value() {
  get_metadata_value "instance/attributes/$1"
}

readonly ACCESS_TOKEN=$(get_metadata_value "instance/service-accounts/default/token" | awk -F\" '{ print $4 }')
readonly PROJECT_ID=$(get_metadata_value "project/project-id")

readonly CONFIG=$(get_attribute_value "runtime-config-name")

readonly SUCCESS_STATUS_PATH="$(get_attribute_value "status-success-base-path")/$(hostname)"
readonly FAILURE_STATUS_PATH="$(get_attribute_value "status-failure-base-path")/$(hostname)"

readonly NODE_PRIVATE_DNS=$(get_metadata_value "instance/hostname")
