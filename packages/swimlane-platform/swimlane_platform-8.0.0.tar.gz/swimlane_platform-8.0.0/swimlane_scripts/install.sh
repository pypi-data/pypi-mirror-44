#!/usr/bin/env bash
#
# Defines shared functions used by different scripts in the Swimlane linux installer

###############################################################################
# Common Constants
###############################################################################

# The Swimlane version
readonly _SW_VERSION="8.0.0"

# Production/Development Docker repo and image tag.
readonly _SW_PROD_DOCKER_IMAGE_REPO_URI=""
readonly _SW_DEV_DOCKER_IMAGE_REPO_URI="nexus.swimlane.io:5000"

# Directories
readonly _SW_ENV_DIR=".secrets"
readonly _SW_DB_INIT_DIR="db-init"
readonly _SW_BACKUP_SCRIPTS_DIR="run-scripts"
readonly _SW_MODULES_DIR="modules"

# Filenames
readonly _SW_COMPOSE_FILE="docker-compose.yml"
readonly _SW_COMPOSE_OVERRIDE_FILE="docker-compose.override.yml"
readonly _SW_COMPOSE_INSTALL_FILE="docker-compose.install.yml"
readonly _SW_DB_INIT_MONGO_SCRIPT="init-mongodb-users.sh"
readonly _SW_API_ENV_FILE=".api-env"
readonly _SW_MONGO_ENV_FILE=".mongo-env"
readonly _SW_TASKS_ENV_FILE=".tasks-env"
readonly _SW_CERT_FILE="swimlane.crt"
readonly _SW_CERT_KEY_FILE="swimlane.key"
readonly _SW_DB_ENCRYPTION_KEY_FILE="database_encryption.key"
readonly _SW_BACKUP_TARBALL="run-files.tar.gz"

###############################################################################
# Common Functions
###############################################################################

# _die()
#
# Usage:
#   _die printf "Error message. Variable: %s\n" "$0"
#
# A simple function for exiting with an error after executing the specified
# command. The command is expected to print a message and should typically
# be either `echo`, `printf`, or `cat`.
_die() {
  # Prefix die message with "cross mark (U+274C)", often displayed as a red x.
  printf "❌  "
  "${@}" 1>&2
  exit 1
}

# _require_argument()
#
# Usage:
#   _require_argument <option> <argument>
#
# If <argument> is blank or another option, print an error message and  exit
# with status 1.
_require_argument() {
  local option="${1:-}"
  local argument="${2:-}"

  if [[ -z "${argument}" ]] || [[ "${argument}" =~ ^- ]]; then
    _die printf "ERROR: Option requires a argument: %s\\n" "${option}"
  fi
}

# _edit_template_compose_file()
#
# Usage:
#   _edit_template_compose_file <file> <repository> <tag>
#
# Edits the specified compose file with the given repository and tag.
_edit_template_compose_file() {
  local file="${1:-}"
  local repository="${2:-}"
  local tag="${3:-}"

  local -r extension=".bak"
  local -r _SW_DOCKER_IMAGE_REPO_PLACEHOLDER="<sw_docker_image_repo_placeholder>"
  local -r _SW_DOCKER_IMAGE_TAG_PLACEHOLDER="<sw_docker_image_tag_placeholder>"

  sed -i${extension} "s|${_SW_DOCKER_IMAGE_REPO_PLACEHOLDER}|${repository}|g" "${file}"
  sed -i${extension} "s|${_SW_DOCKER_IMAGE_TAG_PLACEHOLDER}|${tag}|g" "${file}"

  rm "${file}${extension}"
}

#
# Usage:
#   install [--options] [<arguments>]
#

set -o nounset
set -o errexit
trap '_print_sw "Aborting due to errexit on line $LINENO. Exit code: $?\\n" >&2' ERR
set -o errtrace
set -o pipefail
IFS=$'\n\t'
_ME=$(basename "${0}")

###############################################################################
# Constants
###############################################################################
readonly _DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
readonly _SW_INSTALL_PARENT_DIR="/opt"
readonly _SW_INSTALL_DIR="${_SW_INSTALL_PARENT_DIR}/swimlane"
readonly _SW_INSTALL_SECRETS_DIR="${_SW_INSTALL_DIR}/.secrets"
readonly _SW_INSTALL_DB_INIT_DIR="${_SW_INSTALL_DIR}/db-init"
readonly _SW_INSTALL_BACKUP_DIR="${_SW_INSTALL_DIR}/run-scripts"

readonly _MONGO_ADMIN_PW_PLACEHOLDER="<mongo-admin-password-placeholder>"
readonly _MONGO_SW_PW_PLACEHOLDER="<mongo-sw-password-placeholder>"

readonly _DOCKER_HUB_URI="index.docker.io"
readonly _SW_MONGO_CONTAINER="sw_mongo"

readonly _SW_API_TASKS_UID_GID="2000"
readonly _SW_WEB_UID_GID="2000"
readonly _SW_SECRETS_DIR_PERMS="700"
readonly _SW_SECRETS_FILE_PERMS="600"
readonly _SW_CERT_PERMS="664"

readonly _MIN_SUPPORTED_CENTOS_VERSION="7.5.1804"
readonly _MIN_SUPPORTED_DOCKER_VERSION="18.06.0"
readonly _MIN_SUPPORTED_COMPOSE_VERSION="1.22.0"


###############################################################################
# Help
###############################################################################

# _print_help()
#
# Usage:
#   _print_help
#
# Print the program help information.
_print_help() {
  cat <<HEREDOC
Installs Swimlane ${_SW_VERSION}.

Supported operating systems:
  CentOS ${_MIN_SUPPORTED_CENTOS_VERSION} or greater

NOTE: any bash special characters in arguments must be escaped, or
        alternatively can be passed to this script inside single quotes.

Usage:
  ${_ME} [--options] [<arguments>]
  ${_ME} -h | --help

Optional Flags:
  -h --help               Display this help information.
  --version               Display the Swimlane installer version and exit.
  --generate-cert         Generates a self-signed certificate to use for https
                            access to the Swimlane web interface. Cannot be
                            used with the --cert or --cert-key arguments.
  --mongo-selfsigned-cert Use a self-signed certificate to use for SSL
                            connection between Swimlane and MongoDB.

Optional Arguments:
  --log                   Creates an install log with the provided 
                            filename/location.
  --cert                  Path to the certificate to use for https access to
                            the Swimlane web interface. If specified, the 
                            --cert-key argument must also be provided. Cannot
                            be used with the --generate-cert flag.
  --cert-key              Path to the private key for the provided certificate 
                            from the --cert argument. Cannot be used with the
                            --generate-cert flag.
  --db-encryption-key     The encryption key to use for Swimlane databases.
  --mongo-admin-password  The password of the mongo admin user to create.
  --mongo-sw-password     The password of the mongo Swimlane user to create.
  --install-template-folder     Location of templates for docker-compose and env files.
  --offline-images        Location of zipped docker images for offline install.
  --mongo-trusted-cert    Path to a trusted certificate to use for SSL
                            connection between Swimlane and MongoDB.
                            Cannot be used with the --mongo-selfsigned-cert
                            flag.

Special Arguments/Flags:
  --dev                   Enables installer development mode, pulling
                            development Docker images from the development
                            image repo.
  --image-tag             Must be used with the --dev flag. If set, pulls
                            this specific tag from the development Docker image
                            repo.
HEREDOC
}

###############################################################################
# Parse Options
###############################################################################

# Initialize program option variables.
_ARG_PRINT_HELP=0
_ARG_PRINT_VERSION=0
_ARG_DEV_MODE=0

# Initialize additional expected option variables.
_ARG_LOG=""
_ARG_GENERATE_CERT=0
_ARG_CERT=""
_ARG_CERT_KEY=""
_ARG_DB_ENCRYPTION_KEY=""
_ARG_MONGO_ADMIN_PASSWORD=""
_ARG_MONGO_SW_PASSWORD=""
_ARG_IMAGE_TAG=""
_ARG_SW_DOCKER_IMAGES=""
_ARG_SW_TEMPLATE_DIR=""


while [[ ${#} -gt 0 ]]
do
  __option="${1:-}"
  __maybe_param="${2:-}"
  case "${__option}" in
    -h|--help)
      _ARG_PRINT_HELP=1
      ;;
    --version)
      _ARG_PRINT_VERSION=1
      ;;
    --dev)
      _ARG_DEV_MODE=1
      ;;
    --log)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_LOG="${__maybe_param}"
      shift
      ;;
    --generate-cert)
      _ARG_GENERATE_CERT=1
      ;;
    --cert)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_CERT="${__maybe_param}"
      shift
      ;;
    --cert-key)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_CERT_KEY="${__maybe_param}"
      shift
      ;;
    --db-encryption-key)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_DB_ENCRYPTION_KEY="${__maybe_param}"
      shift
      ;;
    --mongo-admin-password)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_MONGO_ADMIN_PASSWORD="${__maybe_param}"
      shift
      ;;
    --mongo-sw-password)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_MONGO_SW_PASSWORD="${__maybe_param}"
      shift
      ;;
    --image-tag)
      _require_argument "${__option}" "${__maybe_param}"
      _ARG_IMAGE_TAG="${__maybe_param}"
      shift
      ;;
    --offline-images)
       _require_argument "${__option}" "${__maybe_param}"
      _ARG_SW_DOCKER_IMAGES="${__maybe_param}"
      shift
      ;;
    --install-template-folder)
       _require_argument "${__option}" "${__maybe_param}"
      _ARG_SW_TEMPLATE_DIR="${__maybe_param}"
      shift
      ;;
    --endopts)
      # Terminate option parsing.
      break
      ;;
    -*)
      printf "INFO: Unexpected option: %s\\n" "${__option}"
      ;;
  esac
  shift
done

###############################################################################
# Primary Program Functions
###############################################################################

_perform_preflight_checks() {
  # fail if OS is not CentOS
  if [[ $(_get_os) -ne "${_OS_CENTOS}" ]]; then
    _die _print_sw "ERROR: Operating system must be CentOS version ${_MIN_SUPPORTED_CENTOS_VERSION} or greater.\\n"
  fi

  # display warning if running as root
  if [[ $(_current_user_is_root) == true ]]; then
    _print_sw "
********************************************************************************
  WARNING: Installer is currently running as root (sudo).
  
    This is NOT RECOMMENDED!
    
  It is recommended to run the Swimlane installer as the same user that will
    run Swimlane. This user should be a non-root user that has permission to
    write to the ${_SW_INSTALL_DIR} directory and is in the 'docker' group.
********************************************************************************\\n\\n" true

    read -p "Do you still wish to continue? [y/n]: " -n 1 -r
    _print_term "\\n"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      _print_sw "Warning overridden, continuing Swimlane install process.\\n\\n"
    else
      _print_sw "Exiting Swimlane installer.\\n"
      exit 1
    fi
  fi

  # define variables needed to perform checks
  local installed_docker_version
  local installed_compose_version
  local logged_into_docker_hub
  local logged_into_dev_docker_repo
  local has_access_to_sw_images
  local installer_is_offline
  installed_docker_version=$(_get_installed_docker_version)
  installed_compose_version=$(_get_installed_compose_version)
  logged_into_docker_hub=$(_logged_into_docker_repo "${_DOCKER_HUB_URI}")
  logged_into_dev_docker_repo=$(_logged_into_docker_repo "${_SW_DEV_DOCKER_IMAGE_REPO_URI}")
  has_access_to_sw_images=$(_has_access_to_sw_images)
  installer_is_offline=$(_installer_is_offline)

  local errors=()
  # check if we have permission to write to $PWD
  if [[ -d "$PWD" && ! -w "$PWD" ]]; then
    errors+=("ERROR: Installer does not have permission to download files to $PWD.")
  fi

  # check if we have permission to install in /opt/swimlane/
  if [[ -d "${_SW_INSTALL_DIR}" && ! -w "${_SW_INSTALL_DIR}" ]]; then
    errors+=("ERROR: Installer does not have permission to install to ${_SW_INSTALL_DIR}.")
  fi

  # check if we have permission to install in /opt
  if [[ ! -d "${_SW_INSTALL_DIR}" && ! -w "${_SW_INSTALL_PARENT_DIR}" ]]; then
    errors+=("ERROR: ${_SW_INSTALL_DIR} does not exist and the installer does not have
      permission to create it.")
  fi

  # fail if Docker is not installed
  if [[ ${installed_docker_version} -eq ${_DOCKER_INSTALL_NO_VERSION} ]]; then
    errors+=("ERROR: Docker not found. Please install Docker version ${_MIN_SUPPORTED_DOCKER_VERSION} or greater.")
  fi

  # fail if unsupported version of Docker is installed
  if [[ ${installed_docker_version} -eq ${_DOCKER_INSTALL_UNSUPPORTED_VERSION} ]]; then
    errors+=("ERROR: Unsupported version of Docker detected. Please install Docker version ${_MIN_SUPPORTED_DOCKER_VERSION} or greater.")
  fi

  # fail if supported version of Docker is installed but installer doesn't
  # have permission to run docker commands
  if [[ ${installed_docker_version} -eq ${_DOCKER_INSTALL_SUPPORTED_VERSION} ]] \
    && ! docker image ls >& /dev/null
  then
    errors+=("ERROR: Installer cannot run Docker commands. Please ensure that docker is
      running and the installer is run as a user in the 'docker' group.")
  fi

  # fail if docker-compose is not installed
  if [[ ${installed_compose_version} -eq ${_COMPOSE_INSTALL_NO_VERSION} \
    && ! -f /usr/local/bin/docker-compose ]]
  then
    errors+=("ERROR: docker-compose not found. Please install docker-compose version ${_MIN_SUPPORTED_COMPOSE_VERSION} or greater.")
  fi

  # fail if pip is not installed
  if [[ $(_pip_is_installed) == false ]]; then
    errors+=("ERROR: pip not found. Please install pip.")
  fi

  if ! yum list installed python-devel > /dev/null 2>&1; then
    errors+=("ERROR: Package 'python-devel' not found. Please install 'python-devel' using
      the following command:
        yum install python-devel")
  fi

  # fail if unsupported version of docker-compose is installed
  if [[ ${installed_compose_version} -eq ${_COMPOSE_INSTALL_UNSUPPORTED_VERSION} ]]; then
    errors+=("ERROR: Unsupported version of docker-compose detected. Please install
      docker-compose version ${_MIN_SUPPORTED_COMPOSE_VERSION} or greater.")
  fi

  # fail if docker-compose is not on path but found in /usr/local/bin 
  if [[ ${installed_compose_version} -eq ${_COMPOSE_INSTALL_NO_VERSION} \
    && -f /usr/local/bin/docker-compose ]]
  then
    errors+=("ERROR: docker-compose was found in /usr/local/bin/, but not found in the
      current user's path (possibly due to sudo). Please add docker-compose to
      the path and rerun this installer. If running as sudo, consider adding
      symbolic link as in the following example:
        sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose")
  fi

  # fail if --generate-cert is used but openssl is not installed
  if [[ "${_ARG_GENERATE_CERT}" -eq 1 && $(_openssl_is_installed) = false ]]; then
    errors+=("ERROR: The --generate-cert flag was used but openssl is not installed.
      Please install openssl if you wish to generate self-signed certificates.")
  fi

  # when --generate-cert is used, neither --cert or --cert-key arguments can be provided 
  if [[ "${_ARG_GENERATE_CERT}" -eq 1 \
    && (! -z "${_ARG_CERT}" || ! -z "${_ARG_CERT_KEY}") ]]
  then
    errors+=("ERROR: The --cert and --cert-key arguments cannot be used with the
        --generate-cert flag.")
  fi

  # if --cert or --cert-key is used, both must be
  if [[ (! -z "${_ARG_CERT}" && -z "${_ARG_CERT_KEY}")
    || (-z "${_ARG_CERT}" && ! -z "${_ARG_CERT_KEY}") ]]
  then
    errors+=("ERROR: Only one of the --cert and --cert-key arguments were provided. If
      either the --cert or --cert-key arguments are provided, then both must be.")
  fi

  # if --cert is used, must be a path to a valid readable file
  if [[ ! -z "${_ARG_CERT}" && ! -r "${_ARG_CERT}" ]]; then
    errors+=("ERROR: The --cert argument is not a path to a valid readable file.")
  fi

  # if --cert-key is used, must be a path to a valid file
  if [[ ! -z "${_ARG_CERT_KEY}" && ! -f "${_ARG_CERT_KEY}" ]]; then
    errors+=("ERROR: The --cert-key argument is not a path to a valid file.")
  fi

  # if --cert-key is used and isn't readable, it must already be in the expected location
  if [[ ! -z "${_ARG_CERT_KEY}" && -f "${_ARG_CERT_KEY}" && ! -r "${_ARG_CERT_KEY}" \
    && ! "${_ARG_CERT_KEY}" -ef "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}" ]]
  then
    errors+=("ERROR: The --cert-key argument was a path to a valid file, but the file
      is not readable and so it cannot be copied to the expected location. Please move
      the certificate key to ${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}")
  fi

  if [[ ${installer_is_offline} = false \
    && ${_ARG_DEV_MODE} -eq 0 \
    && ${logged_into_docker_hub} = false ]]
  then
    errors+=("ERROR: The user running the installer is not logged in to Docker Hub. Please
      login to Docker Hub by running the following command (run as sudo if you
      are running the installer as sudo):
          docker login")
  fi

  if [[ ${installer_is_offline} = false \
    && ${_ARG_DEV_MODE} -eq 0 \
    && ${logged_into_docker_hub} = true \
    && ${has_access_to_sw_images} = false ]]
  then
    errors+=("ERROR: The user running the installer is logged in to Docker Hub but does
      not have access to Swimlane images. Please login to Docker Hub as a user
      that has access to Swimlane images by running the following commands (run
      as sudo if you are running the installer as sudo):
          docker logout
          docker login")
  fi

  if [[ ${installer_is_offline} = false \
    && ${_ARG_DEV_MODE} -eq 1 \
    && ${logged_into_dev_docker_repo} = false ]]
  then
    errors+=("ERROR: DEV_MODE is enabled but the user running the installer is not logged
      in to the development Docker image repo. Please run the following command
      (run as sudo if you are running the installer as sudo):
          docker login ${_SW_DEV_DOCKER_IMAGE_REPO_URI}")
  fi

  # _ARG_IMAGE_TAG only valid when used with _ARG_DEV_MODE.
  # in other words, in production mode, always use production image tags.
  if [[ ${_ARG_DEV_MODE} -eq 0 && ! -z "${_ARG_IMAGE_TAG}" ]]; then
    errors+=("ERROR: Cannot use _ARG_IMAGE_TAG without also setting _ARG_DEV_MODE.")
  fi

  if [[ "${#errors[@]}" -ne 0 ]]; then
    local messages
    messages=$(_join_by "\\n\\n    " "${errors[@]}")
    _print_sw "
********************************************************************************
  ERROR: One or more issues were detected while performing Swimlane installer
    pre-flight checks. Please address these issues and rerun the installer:\\n
    ${messages}
********************************************************************************\\n\\n" true
    exit 1
  fi
}

_install_swimlane_files() {
  # make install directories
  if [[ ! -d "${_SW_INSTALL_DIR}" ]]; then
    mkdir "${_SW_INSTALL_DIR}"
  fi

  if [[ ! -d "${_SW_INSTALL_SECRETS_DIR}" ]]; then
    mkdir "${_SW_INSTALL_SECRETS_DIR}"
  fi

  if [[ ! -d "${_SW_INSTALL_DB_INIT_DIR}" ]];then
    mkdir "${_SW_INSTALL_DB_INIT_DIR}"
  fi

  # copy compose files
  if [[ ! -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_COMPOSE_FILE}" "${_SW_INSTALL_DIR}"
  fi

  if [[ ! -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_INSTALL_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_COMPOSE_INSTALL_FILE}" "${_SW_INSTALL_DIR}"
  fi

  if [[ ! -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_OVERRIDE_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_COMPOSE_OVERRIDE_FILE}" "${_SW_INSTALL_DIR}"
  fi

  # copy db-init scripts
  if [[ ! -f "${_SW_INSTALL_DB_INIT_DIR}/${_SW_DB_INIT_MONGO_SCRIPT}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_DB_INIT_DIR}/${_SW_DB_INIT_MONGO_SCRIPT}" "${_SW_INSTALL_DB_INIT_DIR}"
  fi

  # copy env files
  if [[ ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_API_ENV_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_ENV_DIR}/${_SW_API_ENV_FILE}" "${_SW_INSTALL_SECRETS_DIR}"
  fi

  if [[ ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_MONGO_ENV_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_ENV_DIR}/${_SW_MONGO_ENV_FILE}" "${_SW_INSTALL_SECRETS_DIR}"
  fi

  if [[ ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_TASKS_ENV_FILE}" ]]; then
    cp "${_ARG_SW_TEMPLATE_DIR}/${_SW_ENV_DIR}/${_SW_TASKS_ENV_FILE}" "${_SW_INSTALL_SECRETS_DIR}"
  fi
}

_setup_swimlane_env() {
  # setup database encryption key if not already setup
  if [[ ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_DB_ENCRYPTION_KEY_FILE}" ]]; then
    local db_encryption_key
    if [[ -z "${_ARG_DB_ENCRYPTION_KEY}" ]]; then
      _print_term "\\nSet database encryption key: The key that will be used to encrypt sensitive Swimlane data.\\n"
      db_encryption_key=$(_collect_input "Database Encryption Key" true)
    else
      db_encryption_key="${_ARG_DB_ENCRYPTION_KEY}"
    fi

    echo "${db_encryption_key}" > "${_SW_INSTALL_SECRETS_DIR}/${_SW_DB_ENCRYPTION_KEY_FILE}"
  else
    _print_sw "Database encryption key has already been configured, please manually edit
  ${_SW_INSTALL_SECRETS_DIR}/${_SW_DB_ENCRYPTION_KEY_FILE} to modify it if needed.\\n"
  fi

  # setup Swimlane env file if not already setup
  if [[ $(_sw_env_file_is_completed) = false ]]; then
    local mongo_admin_password
    if [[ -z "${_ARG_MONGO_ADMIN_PASSWORD}" ]]; then
      _print_term "\\nSet the MongoDB administrator user password: The password to use for the MongoDB 'Admin' user.\\n"
      mongo_admin_password=$(_collect_input "MongoDB Admin user password" true)
    else
      mongo_admin_password="${_ARG_MONGO_ADMIN_PASSWORD}"
    fi

    local mongo_sw_password
    if [[ -z "${_ARG_MONGO_SW_PASSWORD}" ]]; then
      _print_term "\\nSet the MongoDB Swimlane user password: The password to use for the MongoDB 'Swimlane' user.\\n"
      mongo_sw_password=$(_collect_input "MongoDB Swimlane user password" true)
    else
      mongo_sw_password="${_ARG_MONGO_SW_PASSWORD}"
    fi

    # escape mongo_sw_password for api/tasks env files (because these files use a connection string env var)
    local escaped_mongo_sw_password
    escaped_mongo_sw_password=$(_escape_mongo_connection_string "${mongo_sw_password}")

    # populate _SW_API_ENV_FILE
    sed -i "s|${_MONGO_SW_PW_PLACEHOLDER}|${escaped_mongo_sw_password}|g" "${_SW_INSTALL_SECRETS_DIR}/${_SW_API_ENV_FILE}"

    # populate _SW_MONGO_ENV_FILE
    sed -i "s|${_MONGO_ADMIN_PW_PLACEHOLDER}|${mongo_admin_password}|g" "${_SW_INSTALL_SECRETS_DIR}/${_SW_MONGO_ENV_FILE}"
    sed -i "s|${_MONGO_SW_PW_PLACEHOLDER}|${mongo_sw_password}|g" "${_SW_INSTALL_SECRETS_DIR}/${_SW_MONGO_ENV_FILE}"

    # populate _SW_TASKS_ENV_FILE
    sed -i "s|${_MONGO_SW_PW_PLACEHOLDER}|${escaped_mongo_sw_password}|g" "${_SW_INSTALL_SECRETS_DIR}/${_SW_TASKS_ENV_FILE}"
  else
    _print_sw "Secrets have already been configured, please manually edit .env files in
  ${_SW_INSTALL_SECRETS_DIR} to modify them if needed.\\n"
  fi
}

_setup_ssl_certs() {
  # only enter certificate setup if at least one of the installed certificate files is not present
  if [[ ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}" || ! -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}" ]]; then

    # gather user input if flags have not been used
    if [[ "${_ARG_GENERATE_CERT}" -eq 0 \
      && -z "${_ARG_CERT_KEY}" \
      && -z "${_ARG_CERT_KEY}" \
      && $(_openssl_is_installed) = true ]]
    then # openssl is installed, provide option to generate cert
      read -p "Would you like to generate self-signed certificates for Swimlane to use? If not,
  then you must provide paths to an existing certificate and private key. [y/n]: " -n 1 -r
      _print_term "\\n"
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        _ARG_GENERATE_CERT=1
      fi
    fi

    if [[ "${_ARG_GENERATE_CERT}" -eq 1 ]]; then
      # generate self-signed certificate
      openssl req \
        -newkey rsa:2048 -nodes -keyout "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}" \
        -x509 -days 365 -out "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}"
    else # install custom certificates
      # collect path to certificate if required
      if [[ ! -f "${_ARG_CERT}" ]]; then
        _print_term "\\nSet path to the certificate to use for https access to the Swimlane web interface.\\n"

        while true; do
          read -r -p "  Enter path to certificate: " _ARG_CERT
          if [[ -f "${_ARG_CERT}" ]]; then
            break
          else
            _print_term "    Input was not a path to a valid file, please try again.\\n\\n"
          fi
        done
      fi

      # collect path to certificate key if required
      if [[ ! -f "${_ARG_CERT_KEY}" ]]; then
        _print_term "\\nSet path to the private key to use for the previously provided certificate.\\n"

        while true; do
          read -r -p "  Enter path to private key: " _ARG_CERT_KEY
          if [[ -f "${_ARG_CERT_KEY}" ]]; then
            break
          else
            _print_term "    Input was not a path to a valid file, please try again.\\n\\n"
          fi
        done
      fi

      # copy to install directory
      cp "${_ARG_CERT}" "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}"

      # cert key not guaranteed to be readable, so only copy if it is
      if [[ -r "${_ARG_CERT_KEY}" ]]; then
        cp "${_ARG_CERT_KEY}" "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}"
      fi
    fi
  else
    _print_sw "Swimlane SSL certificates have already been configured, please manually replace
  the certificate files at ${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE} and
  ${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE} if needed.\\n"
  fi
}

_get_swimlane_images() {
  if [[ $(_installer_is_offline) = true ]]; then
    # offline installer
    # template compose file already edited by offline installer build, extract docker images
    docker load -i "${_ARG_SW_DOCKER_IMAGES}"
  else
    # online installer
    # edit template compose file
    if [[ ${_ARG_DEV_MODE} -eq 1 && ! -z "${_ARG_IMAGE_TAG}" ]]; then
      # use development image repo and _ARG_IMAGE_TAG
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" "${_SW_DEV_DOCKER_IMAGE_REPO_URI}/" "${_ARG_IMAGE_TAG}"
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_OVERRIDE_FILE}" "${_SW_DEV_DOCKER_IMAGE_REPO_URI}/" "${_ARG_IMAGE_TAG}"
    elif [[ ${_ARG_DEV_MODE} -eq 1 ]]; then
      # use development image repo and default development tag
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" "${_SW_DEV_DOCKER_IMAGE_REPO_URI}/" "${_SW_VERSION}"
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_OVERRIDE_FILE}" "${_SW_DEV_DOCKER_IMAGE_REPO_URI}/" "${_SW_VERSION}"
    else
      # use production image repo and tag
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" "${_SW_PROD_DOCKER_IMAGE_REPO_URI}" "${_SW_VERSION}"
      _edit_template_compose_file "${_SW_INSTALL_DIR}/${_SW_COMPOSE_OVERRIDE_FILE}" "${_SW_PROD_DOCKER_IMAGE_REPO_URI}" "${_SW_VERSION}"
    fi

    docker-compose -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" \
      -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_INSTALL_FILE}" \
      --no-ansi \
      pull
  fi
}

_setup_dbs() {
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # start _SW_MONGO_CONTAINER detached
  # the _SW_COMPOSE_INSTALL_FILE mounts the init scripts
  _print_sw "Starting Swimlane database containers...\\n"
  docker-compose -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" \
    -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_INSTALL_FILE}" \
    --no-ansi \
    up \
    -d \
    "${_SW_MONGO_CONTAINER}"
  _print_sw "Successfully started Swimlane database containers.\\n"
  
  local mongo_success_message="Successfully completed MongoDB initialization for Swimlane."
  local error_message="ERROR: SWIMLANE INITIALIZATION ERROR OCCURRED"

  _check_db_init_status "${_SW_MONGO_CONTAINER}" \
    "${mongo_success_message}" \
    "${error_message}" \
    "${timestamp}"

  # stop _SW_MONGO_CONTAINER
  _print_sw "Stopping Swimlane database containers...\\n"
  docker-compose -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_FILE}" \
    -f "${_SW_INSTALL_DIR}/${_SW_COMPOSE_INSTALL_FILE}" \
    --no-ansi \
    stop
  _print_sw "Successfully stopped Swimlane database containers.\\n"
}

_set_permissions() {
  # check permissions on _SW_INSTALL_SECRETS_DIR
  # if permissions not restricted, try to restrict them
  # print a warning if permissions setting fails
  if [[ $(_file_has_permissions "${_SW_INSTALL_SECRETS_DIR}" "${_SW_SECRETS_DIR_PERMS}") = false ]] \
    && ! chmod "${_SW_SECRETS_DIR_PERMS}" "${_SW_INSTALL_SECRETS_DIR}"
  then
    _print_sw "
********************************************************************************
  WARNING: Installer could not restrict permissions on ${_SW_INSTALL_SECRETS_DIR}.
  
    If you would like to protect Swimlane secrets from being read by
      unauthorized users on this machine, please set the permissions on
      ${_SW_INSTALL_SECRETS_DIR} after Swimlane installation is complete by
      running the following command:

          chmod ${_SW_SECRETS_DIR_PERMS} ${_SW_INSTALL_SECRETS_DIR}
********************************************************************************\\n" true
  fi

  # set permissions on _SW_CERT
  if [[ $(_file_has_permissions "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}" "${_SW_CERT_PERMS}") = false ]] \
    && ! chmod "${_SW_CERT_PERMS}" "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}"
  then
    _print_sw "
********************************************************************************
  WARNING: Installer could not set permissions on ${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}.
  
    This file MUST be open to read by others, or installation will fail. Please,
      ensure that users/groups other than the file owner are able to read this
      file. The following command can be used to set the permissions:

          chmod ${_SW_CERT_PERMS} ${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_FILE}
********************************************************************************\\n" true
  fi

  # check permissions on environment files
  # if permissions not restricted, try to restrict them
  local env_files=("${_SW_INSTALL_SECRETS_DIR}/${_SW_API_ENV_FILE}" \
    "${_SW_INSTALL_SECRETS_DIR}/${_SW_MONGO_ENV_FILE}" \
    "${_SW_INSTALL_SECRETS_DIR}/${_SW_TASKS_ENV_FILE}")

  local filename
  local warning_filenames=()
  for filename in "${env_files[@]}"; do
    if [[ $(_file_has_permissions "${filename}" "${_SW_SECRETS_FILE_PERMS}") = false ]] \
      && ! chmod "${_SW_SECRETS_FILE_PERMS}" "${filename}"
    then
      warning_filenames+=("${filename}")
    fi
  done

  # print a warning if permissions setting on environment files fails
  if [[ "${#warning_filenames[@]}" -ne 0 ]]; then
    local filenames
    filenames=$(_join_by "\\n        * " "${warning_filenames[@]}")
    _print_sw "
********************************************************************************
  WARNING: Installer could not restrict permissions on one or more environment files
    in ${_SW_INSTALL_SECRETS_DIR}. Permissions on the following files
    could not be set:
        * ${filenames}

    The following command can be used to restrict the permissions:
          chmod ${_SW_SECRETS_FILE_PERMS} <insert filename here>
********************************************************************************\\n" true
  fi

  # chown database encryption key to the Swimlane API/Tasks UID/GID
  _set_secret_ownership_and_permissions "${_SW_INSTALL_SECRETS_DIR}/${_SW_DB_ENCRYPTION_KEY_FILE}" \
    "${_SW_API_TASKS_UID_GID}" \
    "${_SW_SECRETS_FILE_PERMS}"
  
  # chown cert private key to the Swimlane Web UID/GID
  _set_secret_ownership_and_permissions "${_SW_INSTALL_SECRETS_DIR}/${_SW_CERT_KEY_FILE}" \
    "${_SW_WEB_UID_GID}" \
    "${_SW_SECRETS_FILE_PERMS}"
}

###############################################################################
# Secondary Program Functions
###############################################################################

readonly _OS_UNSUPPORTED=0
readonly _OS_CENTOS=1
_get_os() {
  local os="${_OS_UNSUPPORTED}"

  if [[ -f /etc/centos-release ]]; then
    local version_file_contents
    version_file_contents=$(cat /etc/centos-release)
    local centos_version
    centos_version=$(_get_semver_from_string "${version_file_contents}")

    if [[ $(_version_is_greater_than_or_equal_to_min_version \
      "${centos_version}" "${_MIN_SUPPORTED_CENTOS_VERSION}") = true ]]
    then
      os="${_OS_CENTOS}"
    fi
  fi

  echo "${os}"
}

readonly _DOCKER_INSTALL_NO_VERSION=0
readonly _DOCKER_INSTALL_SUPPORTED_VERSION=1
readonly _DOCKER_INSTALL_UNSUPPORTED_VERSION=2
_get_installed_docker_version() {
  local installed_docker_version="${_DOCKER_INSTALL_NO_VERSION}"

  if command -v docker > /dev/null; then
    local docker_version_output
    docker_version_output=$(docker --version)
    local docker_version
    docker_version=$(_get_semver_from_string "${docker_version_output}")

    if [[ $(_version_is_greater_than_or_equal_to_min_version \
      "${docker_version}" "${_MIN_SUPPORTED_DOCKER_VERSION}") = true ]]
    then
      installed_docker_version="${_DOCKER_INSTALL_SUPPORTED_VERSION}"
    else
      installed_docker_version="${_DOCKER_INSTALL_UNSUPPORTED_VERSION}"
    fi
  fi

  echo "${installed_docker_version}"
}

readonly _COMPOSE_INSTALL_NO_VERSION=0
readonly _COMPOSE_INSTALL_SUPPORTED_VERSION=1
readonly _COMPOSE_INSTALL_UNSUPPORTED_VERSION=2
_get_installed_compose_version() {
  local installed_compose_version="${_COMPOSE_INSTALL_NO_VERSION}"

  if command -v docker-compose > /dev/null; then
    # get version, i.e. '1.22.1,'
    local compose_version
    compose_version=$(docker-compose --version | cut -d' ' -f3)
    # remove trailing comma
    compose_version=${compose_version::-1}

    if [[ $(_version_is_greater_than_or_equal_to_min_version \
      "${compose_version}" "${_MIN_SUPPORTED_COMPOSE_VERSION}") = true ]]
    then
      installed_compose_version="${_COMPOSE_INSTALL_SUPPORTED_VERSION}"
    else
      echo "got here" >> test.log
      installed_compose_version="${_COMPOSE_INSTALL_UNSUPPORTED_VERSION}"
    fi
  fi

  echo "${installed_compose_version}"
}

_openssl_is_installed() {
  if command -v openssl > /dev/null; then
    echo true
  else
    echo false
  fi
}

_pip_is_installed() {
  if command -v pip > /dev/null; then
    echo true
  else
    echo false
  fi
}

_current_user_is_root() {
  if [[ "$EUID" -eq 0 ]]; then
    echo true
  else
    echo false
  fi
}

_logged_into_docker_hub() {
  if [[ -f ~/.docker/config.json ]] \
    && grep -Fq "${_DOCKER_HUB_URI}" ~/.docker/config.json
  then
    echo true
  else
    echo false
  fi
}

_logged_into_docker_repo() {
  local repo="${1:-}"

  if [[ -f ~/.docker/config.json ]] \
    && grep -Fq "${repo}" ~/.docker/config.json
  then
    echo true
  else
    echo false
  fi
}

_has_access_to_sw_images() {
  if [[ $(_logged_into_docker_hub) = true ]]; then
    # get auth token from ~/.docker/config.json
    local docker_config
    docker_config=$(cat ~/.docker/config.json)

    # "                   match the quote at the start of the key
    # (https:\/\/)?       match 0 or 1 instances of "https://"
    # index\.docker\.io   match "index.docker.io"
    # (\/v1\/)?           match 0 or 1 instances of "/v1/"
    # ":\s*\{             match the end of the key line 
    # \s*"auth":\s*       match the beginning of the token line
    # "([^"]*)"           capture the token (all characters within the quote)
    # ,?\s*\}             match the end of the json property, optionally with a comma
    local auth_token_regex='"(https:\/\/)?index\.docker\.io(\/v1\/)?":\s*\{\s*"auth":\s*"([^"]*)",?\s*\}'
    if [[ "${docker_config}" =~ ${auth_token_regex} ]]; then
      # get auth token from regex capture group 3
      local auth_token="${BASH_REMATCH[3]}"

      # if this curl fails, then the user cannot pull swimlane images
      if curl --silent -f \
        https://index.docker.io/v1/repositories/swimlane/swimlane-api/tags \
        -H "Authorization: Basic ${auth_token}"
      then
        echo true
        return
      fi
    fi
  fi
  echo false
}

_sw_env_file_is_completed() {
  if [[ -f "${_SW_INSTALL_SECRETS_DIR}/${_SW_API_ENV_FILE}" ]] \
    && ! grep -Fq "${_MONGO_SW_PW_PLACEHOLDER}" "${_SW_INSTALL_SECRETS_DIR}/${_SW_API_ENV_FILE}"
  then
    echo true
  else
    echo false
  fi
}

_escape_mongo_connection_string() {
  local password="${1:-}"

  local escaped_password=${password//@/%40}
  echo "${escaped_password}"
}

readonly _DB_INIT_ERROR_EXIT_CODE=64
_check_db_init_status() {
  local container="${1:-}"
  local success_message="${2:-}"
  local error_message="${3:-}"
  local timestamp="${4:-}"

  _print_sw "Starting initialization detection for ${container}...\\n"

  # only enter log scanning if there is not already a success message in the logs
  if ! docker logs "${container}" 2>&1 | grep -Fq "${success_message}"; then
    _print_sw "Scanning ${container} logs for initialization success or error...\\n"

    # temporarily turn off errexit so we can give a helpful error message based
    # on the timeout process exit code
    set +o errexit

    # temporarily turn off pipefail so we can kill the `docker logs` process
    # without the timeout process exiting with an error code
    set +o pipefail

    local timeout_exit_code
    local logline
    timeout 30 docker logs -f --since "${timestamp}" "${container}" 2>&1 | while read -r logline
    do
      # if success message detected, pkill the `docker logs` process and continue.
      # '$(pgrep -P $$ timeout)' gets the pid of the timeout process to use to 
      # kill the `docker logs` process (timeout is the parent).
      # this exits the loop.
      [[ "${logline}" == *"${success_message}"* ]] && pkill -P "$(pgrep -P $$ timeout)" docker && exit 0

      # if error message detected, exit the timeout process
      [[ "${logline}" == *"${error_message}"* ]] && exit ${_DB_INIT_ERROR_EXIT_CODE}
    done

    # last exit code is 1 in the event of a timeout
    # last exit code is ${_DB_INIT_ERROR_EXIT_CODE} when exiting from error message detected above
    # last exit code is 0 when exiting from success message detected above
    # other exit codes are possible if signals are sent to the timeout process by the user
    # or maybe due to a race case between pkill and exit 0 in the success case?
    timeout_exit_code=$?
    if [[ ${timeout_exit_code} -eq 1 ]]; then
      _die _print_sw "ERROR: Initialization detection timed out. Please delete all Swimlane docker
  containers and volumes and rerun the Swimlane installer. You can do the
  former by running the following command:
      docker-compose -f /opt/swimlane/docker-compose.yml down --volume\\n"
    elif [[ ${timeout_exit_code} -eq ${_DB_INIT_ERROR_EXIT_CODE} ]]; then
      _die _print_sw "ERROR: An error occurred initializing ${container}, please see docker logs for
  ${container} for additional details:
      docker logs ${container}\\n"
    elif [[ ${timeout_exit_code} -ne 0 ]]; then
      _die _print_sw "ERROR: An unexpected error occurred while detecting initialization status for
  ${container}. Please delete all Swimlane docker containers and volumes and
  rerun the Swimlane installer. You can do this by running the following
  command:
      docker-compose -f /opt/swimlane/docker-compose.yml down --volume\\n"
    fi

    # turn back on errexit and pipefail
    set -o errexit
    set -o pipefail
  fi

  _print_sw "Initialization detection for ${container} completed successfully. ${container}
  was successfully initialized.\\n"
}

_set_secret_ownership_and_permissions() {
  local file="${1:-}"
  local desired_owner_uid_gid="${2:-}"
  local desired_perms="${3:-}"

  if chown "${desired_owner_uid_gid}:${desired_owner_uid_gid}" "${file}" > /dev/null 2>&1; then
    # chown succeeded, try to set permissions
    if ! chmod "${desired_perms}" "${file}" > /dev/null 2>&1; then
      # chmod failed, print warning
      _print_sw "
********************************************************************************
  WARNING: Installer could not restrict permissions on ${file}.

    If you would like to protect Swimlane secrets from being read by
      unauthorized users on this machine, please set the permissions on
      ${file} after Swimlane installation is complete
      by running the following command:

        chmod ${desired_perms} ${file}
********************************************************************************\\n\\n" true
    fi
  else
    # chown failed, check whether to print warning or error
    if [[ ! -r "${file}" ]]; then
      _print_sw "
********************************************************************************
  WARNING: Installer could not read the permissions of ${file}.

    If starting Swimlane fails, please run the following commands to set the 
      recommended ownership and permissions on this file:

        sudo chown ${desired_owner_uid_gid}:${desired_owner_uid_gid} ${file}
        sudo chmod ${desired_perms} ${file}
********************************************************************************\\n\\n" true
    elif [[ $(_other_has_read_permission "${file}") = true ]]; then
      # other has read permission, just display a warning
      # this is expected when not running installer as root
      _print_sw "
********************************************************************************
  INFO: Installer could not chown ${file}
    to the UID/GID of the user in the Swimlane containers.

    Others have read permissions for this file, so the Swimlane containers will
      still be able to read the file. However, if read permissions for others
      are ever taken away for this file, then Swimlane will fail to start.
      Please run the following commands to set recommended ownership and
      permissions on this file:

        sudo chown ${desired_owner_uid_gid}:${desired_owner_uid_gid} ${file}
        sudo chmod ${desired_perms} ${file}
********************************************************************************\\n\\n" true
    else
      # other does not have read permission, installer will fail
      _print_sw "
********************************************************************************
  WARNING: Installer could not chown ${file}
    to the UID/GID of the user in the Swimlane containers and others do not have
    read permissions for this file. Swimlane containers will not be able to read
    this required file. Please set permissions on this file to open read
    permissions for others, or run the following commands to set the recommended
    ownership and permissions:
      sudo chown ${desired_owner_uid_gid}:${desired_owner_uid_gid} ${file}
      sudo chmod ${desired_perms} ${file}
********************************************************************************\\n\\n" true
    fi
  fi
}

_installer_is_offline() {
  if [[ -f "${_ARG_SW_DOCKER_IMAGES}" ]]; then
    echo true
  else
    echo false
  fi
}

###############################################################################
# Helper Functions
###############################################################################

_version_is_greater_than_or_equal_to_min_version() {
  local version="${1:-}"
  local min_version="${2:-}"

  # Break apart the versions into an array of semantic parts
  local version_parts
  local min_version_parts
  mapfile -t version_parts < <(echo "${version}" | tr '.' "\\n")
  mapfile -t min_version_parts < <(echo "${min_version}" | tr '.' "\\n")

  # Ensure there are 3 parts (semantic versioning)
  if [[ ${#version_parts[@]} -lt 3 ]] || [[ ${#min_version_parts[@]} -lt 3 ]]; then
    echo false
    return
  fi

  # use parameter expansion to remove any leading zeros
  local major=${version_parts[0]#0}
  local minor=${version_parts[1]#0}
  local patch=${version_parts[2]#0}
  local min_major=${min_version_parts[0]#0}
  local min_minor=${min_version_parts[1]#0}
  local min_patch=${min_version_parts[2]#0}
  # Compare the parts
  if [[ ${major} -lt ${min_major} ]] \
    || [[ ${major} -eq ${min_major} && ${minor} -lt ${min_minor} ]] \
    || [[ ${major} -eq ${min_major} && ${minor} -eq ${min_minor} && ${patch} -lt ${min_patch} ]]
  then
    echo false
    return
  fi

  echo true
}

_collect_input() {
  # shellcheck disable=SC2034 # False unused variable warning
  local name="${1:-}"
  local is_sensitive="${2:-}"

  local silent_flag=""
  if [[ "${is_sensitive}" = true ]]; then
    # shellcheck disable=SC2034 # False unused variable warning
    silent_flag="-s"
  fi

  local input1
  local input2
  while true; do
    eval 'read ${silent_flag} -r -p "  Enter ${name}: " input1'
    _print_term "\\n"
    eval 'read ${silent_flag} -r -p "  Enter ${name} again: " input2'
    _print_term "\\n"

    if [[ ! "${input1}" = "${input2}" ]]; then
      _print_term "    Oops! Inputs did not match, please try again.\\n\\n"
    elif [[ -z "${input1}" ]]; then
      _print_term "    Empty input not allowed, please try again.\\n\\n"
    elif [[ "${input1}" == *" "* ]]; then
      _print_term "    Space character not allowed, please try again.\\n\\n"
    else
      break
    fi
  done
  
  _print_term "\\n"
  echo "${input1}"
}

_file_has_permissions() {
  local file="${1:-}"
  local desired_permissions="${2:-}"

  if [[ $(stat -c "%a" "${file}") -eq "${desired_permissions}" ]]; then
    echo true
  else
    echo false
  fi
}

_other_has_read_permission() {
  local file="${1:-}"

  local perms
  perms=$(stat -c "%a" "${file}")
  # character at 3rd index should be others permissions
  local others_perms=${perms:2:2}
  if [[ ! -z "${others_perms}" && \
    ("${others_perms}" = "4" \
      || "${others_perms}" = "5" \
      || "${others_perms}" = "6" \
      || "${others_perms}" = "7") ]]
  then
    echo true
  else
    echo false
  fi
}

_get_semver_from_string() {
  local string="${1:-}"

  local semver_regex='([0-9]+)\.([0-9]+)\.([0-9]+)'
  if [[ "${string}" =~ ${semver_regex} ]]; then
    echo "${BASH_REMATCH[0]}"
  else
    echo false
  fi
}

_join_by() {
  local delimiter="${1:-}"
  
  shift
  echo -n "$1"
  shift
  printf "%s" "${@/#/$delimiter}"
}

# prints to the terminal only
_print_term() {
  local message="${1:-}"
  printf "${message}" > /dev/tty
}

# prints to the terminal and to the installer log file
_print_sw() {
  local message="${1:-}"
  local omit_timestamp="${2:-}"

  local timestamp
  timestamp="[$(date +"%Y-%m-%dT%H:%M:%S%z")] "
  if [[ "${omit_timestamp}" = true ]]; then
    timestamp=""
  elif [[ "${message}" == *$'\n'* ]]; then
    # format multiline messages with spaces
    local messages_array
    readarray -t messages_array <<<"${message}"
    local first_line="${messages_array[0]}"
    local messages_needing_formatting=("${messages_array[@]:1}")

    # sanity check to make sure _messages_needing_formatting is defined
    # shellcheck disable=SC2128 # False array expansion warning
    if [[ ! -z "${messages_needing_formatting}" ]]; then
      # get timestamp length and generate spaces variable
      local timestamp_length="${#timestamp}"
      local spaces
      spaces=$(head -c "${timestamp_length}" < /dev/zero | tr '\0' ' ')

      # insert spaces at the beginning of each line except the first
      local formatted_messages=("${messages_needing_formatting[@]/#/${spaces}}")
      messages_array=("${first_line}" "${formatted_messages[@]}")
      message=$(_join_by "\\n" "${messages_array[@]}")
    fi
  fi

  if [[ ! -z "${_ARG_LOG}" ]]; then
    printf "${timestamp}${message}" | tee -a "${_ARG_LOG}" > /dev/tty
  else
    printf "${timestamp}${message}" > /dev/tty
  fi
}

_call_with_log_redirect() {
  local func="${1:-}"

  if [[ ! -z "${_ARG_LOG}" ]]; then
    "${func}" >> "${_ARG_LOG}"
  else
    "${func}"
  fi
}

###############################################################################
# Main
###############################################################################

# _main()
#
# Usage:
#   _main [<options>] [<arguments>]
#
# Description:
#   Entry point for the program, handling basic option parsing and dispatching.
_main() {
  if ((_ARG_PRINT_HELP)); then
    _print_help
  elif ((_ARG_PRINT_VERSION)); then
    printf "Swimlane Installer version %s\\n" "${_SW_VERSION}"
  else
    
    if (($(tput cols) >= 135)); then
      _print_term "
               .::
             :::::
           .::::::
         :::::::::
       .::::::::::  ..
      ::::::::::   oooo
      ::::::::  ,0000000o           8888888  8888     888     8888 888  8888     8888 888            8888       8888     888 8888888888
      ::::::oo  o000000000%%.       888888888  8888   88888   8888  888  88888   88888 888           888888      88888    888 8888888888
      :::%%%%000o,  00000%%%%.^^^      8888        8888  88888  8888   888  8888888888888 888          888  888     8888888  888 888
      -%%000000000,  %%%%%%.^^^^^       88888888    888888888888888    888  888 88888 888 888         888    888    888  888 888 8888888888
       o000000000o,  ^^^^^^^^            8888    888888 888888     888  888  888  888 888        888888888888   888   888888 888
         o00000o,  ^^^^^^^^^^      888888888      88888 88888      888  888       888 888888888 8888      8888  888    88888 8888888888
           oooo   ^^^^^^^^^^        8888888        888   888       888  888       888 88888888 8888        8888 888      888 8888888888
                ^^^^^^^^^^
                ^^^^^^^^
                ^^^^^^
                ^^^^
                ^^\\n\\n" true
    else
      _print_sw "
##############################
##### Swimlane Installer #####
##############################\\n\\n" true
    fi

    _print_sw "Welcome to the Swimlane installer! Thank you for choosing Swimlane!\\n\\n"

    _print_sw "Performing installer pre-flight checks...\\n"
    _call_with_log_redirect _perform_preflight_checks
    _print_sw "Installer pre-flight checks completed successfully.\\n\\n"

    _print_sw "Installing Swimlane files...\\n"
    _call_with_log_redirect _install_swimlane_files
    _print_sw "Successfully installed Swimlane files.\\n\\n"

    _print_sw "Setting up Swimlane SSL certificates...\\n"
    _call_with_log_redirect _setup_ssl_certs
    _print_sw "Successfully set up Swimlane SSL certificates.\\n\\n"

    _print_sw "Setting up Swimlane environment configuration...\\n"
    _call_with_log_redirect _setup_swimlane_env
    _print_sw "Successfully set up Swimlane environment configuration.\\n\\n"

    _print_sw "Getting Swimlane images...\\n"
    _call_with_log_redirect _get_swimlane_images
    _print_sw "Successfully got Swimlane images.\\n\\n"

    _print_sw "Setting up Swimlane databases...\\n"
    _call_with_log_redirect _setup_dbs
    _print_sw "Successfully set up Swimlane databases.\\n\\n"

    _print_sw "Setting permissions on installed files...\\n"
    _call_with_log_redirect _set_permissions
    _print_sw "Successfully set permissions on installed files.\\n\\n\\n"
  fi
}

# Call `_main` after everything has been defined.
_main "$@"
