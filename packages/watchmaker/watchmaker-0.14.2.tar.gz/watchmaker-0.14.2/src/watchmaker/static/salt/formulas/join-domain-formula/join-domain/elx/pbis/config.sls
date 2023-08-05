# Customize the PBIS configuration to assure a more sane,
# post-join behavior:
# * Set 'LoginShellTemplate' and 'Local_LoginShellTemplate' to
#   desired (friendlier) value ("/bin/bash" - PBIS defaults to
#   "/bin/sh")
# * Set 'HomeDirTemplate' and 'Local_HomeDirTemplate' to flatter
#   default value ("/home/<DOMAIN>/${USER}" - PBIS defaults to
#   "/home/local/<DOMAIN>/${USER}")
# * Set 'DomainManagerIgnoreAllTrusts' to "true" to prevent
#   spurious service-faults in multi-domain forests.
# * Set 'DomainManagerIncludeTrustsList' to match domain FQDN.
#   This setting is necessary due to setting of the
#   'DomainManagerIgnoreAllTrusts' value to "true"
#
#################################################################
{%- from tpldir ~ '/map.jinja' import join_domain with context %}

{%- for shell in join_domain.pbis_user_shell %}
PBIS-config-Shell-{{ shell }}:
  cmd.run:
    - name: '
        {{ join_domain.install_bin_dir }}/bin/config {{ shell }} "{{ join_domain.login_shell }}";
        ret=$?;
        if [[ $ret -eq 5 ]];
        then
            ret=0;
        fi;
        exit $ret;
    '
    - onlyif: test $({{ join_domain.install_bin_dir }}/bin/config --show {{ shell }} | grep -q -i "{{ join_domain.login_shell }}")$? -ne 0
    - require:
      - pkg: PBIS-install
{%- endfor %}

{%- for home in join_domain.pbis_user_home %}
PBIS-config-Home-{{ home }}:
  cmd.run:
    - name: '
        {{ join_domain.install_bin_dir }}/bin/config {{ home }} "{{ join_domain.login_home }}";
        ret=$?;
        if [[ $ret -eq 5 ]];
        then
            ret=0;
        fi;
        exit $ret;
    '
    - onlyif: test $({{ join_domain.install_bin_dir }}/bin/config --show {{ home }} | grep -q -i "{{ join_domain.login_home }}")$? -ne 0
    - require:
      - pkg: PBIS-install
{%- endfor %}

PBIS-config-TrustIgnore:
  cmd.run:
    - name: {{ join_domain.install_bin_dir }}/bin/config DomainManagerIgnoreAllTrusts true
    - onlyif: test $({{ join_domain.install_bin_dir }}/bin/config --show DomainManagerIgnoreAllTrusts | grep -q -i "true")$? -ne 0
    - require:
      - pkg: PBIS-install

PBIS-config-TrustList:
  cmd.run:
    - name: {{ join_domain.install_bin_dir }}/bin/config DomainManagerIncludeTrustsList {{ join_domain.dns_name }}
    - onlyif: test $({{ join_domain.install_bin_dir }}/bin/config --show DomainManagerIncludeTrustsList | grep -q -i "{{ join_domain.dns_name }}")$? -ne 0
    - require:
      - pkg: PBIS-install

PBIS-disable-NssEnumeration:
  cmd.run:
    - name: '
        {{ join_domain.install_bin_dir }}/bin/config NssEnumerationEnabled false;
        ret=$?;
        if [[ $ret -eq 5 ]];
        then
            ret=0;
        fi;
        exit $ret;
    '
    - onlyif: test $({{ join_domain.install_bin_dir }}/bin/config --show NssEnumerationEnabled | grep -q -i "false")$? -ne 0
    - require:
      - pkg: PBIS-install
