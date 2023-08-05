#! /bin/bash -
# Install system packages required by model package.

source $(dirname $0)/utils.sh

installedpkgs=
pkgstoinstall=

########################################################################
# Check packages already installed.

for pkg in $@; do
  if dpkg-query -s ${pkg} 2>/dev/null | grep 'installed' > /dev/null; then
    installedpkgs+=" ${pkg}"
  else
    pkgstoinstall+=" ${pkg}"
  fi
done

if [[ ! -z ${installedpkgs} ]]; then
  echo
  echo '*** The following required system packages are already installed:'
  echo " ${installedpkgs}"
fi

########################################################################
# Install packages not installed.
# TODO: Do not install recommended system packages.

if [[ ! -z ${pkgstoinstall} ]]; then
  echo
  echo '*** Installing the following system dependencies:'
  echo " ${pkgstoinstall}"

  # sudo apt-get install -y wajig > /dev/null
  # wajig update > /dev/null
  # wajig distupgrade -y > /dev/null

  for pkg in ${pkgstoinstall}; do
    if [[ ! -z ${_MLHUB_OPTION_YES} ]] || _is_yes "\nDo you want to install ${pkg}"; then
      sudo apt-get install -y ${pkg}

      if [[ $? -ne 0 ]]; then
        exit 1
      fi

    # Or:
    # wajig install -y ${pkg}

    fi
  done
fi
