%global release_name liberty
%global release_ver liberty-rc1

Name:          openstack-murano
Version:       XXX
Release:       XXX
Summary:       OpenStack Murano
Group:         Applications/System
License:       Apache License, Version 2.0
URL:           https://launchpad.net/murano
Obsoletes:     murano < 0.5
Provides:      murano
#Sources
Source0:       https://launchpad.net/murano/%{release_name}/%{release_ver}/+download/murano-%{version}.tar.gz
Source1:       murano-api.service
Source2:       murano-engine.service
Source3:       murano.logrotate
Source4:       murano-cf-api.service
#Patches:

BuildArch:     noarch
# Build dependencies
BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-jsonschema
BuildRequires: python-keystonemiddleware
BuildRequires: python-oslo-config
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-messaging
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-service
BuildRequires: python-oslo-sphinx
BuildRequires: python-pbr
BuildRequires: python-setuptools
BuildRequires: python-sphinx
BuildRequires: python-sphinxcontrib-httpdomain
BuildRequires: systemd-units


%description
Murano Project introduces an application catalog, which allows application developers and cloud
administrators to publish various cloud-ready applications in a browsable‎ categorised catalog, which may be used by the cloud
users (including the inexperienced ones) to pick-up the needed applications and services and composes the reliable environments
out of them in a "push-the-button" manner

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-engine = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}
Requires: %{name}-cf-api = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}

# MURANO-COMMON
%package common
Summary: Murano common
Group: System Environment/Base
Requires:      python-alembic >= 0.8.0
Requires:      python-babel >= 1.3
Requires:      python-eventlet >= 0.17.4
Requires:      python-iso8601 >= 0.1.9
Requires:      python-jsonpatch >= 1.1
Requires:      python-jsonschema >= 2.0.0
Requires:      python-keystonemiddleware >= 2.0.0
Requires:      python-kombu >= 3.0.7
Requires:      python-netaddr >= 0.7.12
Requires:      python-oslo-config >= 2:2.3.0
Requires:      python-oslo-context >= 0.2.0
Requires:      python-oslo-db >= 2.4.1
Requires:      python-oslo-i18n >= 1.5.0
Requires:      python-oslo-log >= 1.8.0
Requires:      python-oslo-messaging >= 1.16.0
Requires:      python-oslo-middleware >= 2.8.0
Requires:      python-oslo-policy >= 0.5.0
Requires:      python-oslo-serialization >= 1.4.0
Requires:      python-oslo-service >= 0.7.0
Requires:      python-oslo-utils >= 2.0.0
Requires:      python-paste
Requires:      python-paste-deploy >= 1.5.0
Requires:      python-pbr >= 1.6
Requires:      python-psutil >= 1.1.1
Requires:      python-congressclient >= 1.0.0
Requires:      python-heatclient >= 0.3.0
Requires:      python-keystoneclient >= 1:1.6.0
Requires:      python-mistralclient >= 1.0.0
Requires:      python-muranoclient >= 0.7.0
Requires:      python-neutronclient >= 2.6.0
Requires:      PyYAML >= 3.1.0
Requires:      python-retrying >= 1.2.3
Requires:      python-routes >= 1.12.3
Requires:      python-semantic_version >= 2.3.1
Requires:      python-six >= 1.9.0
Requires:      python-stevedore >= 1.5.0
Requires:      python-sqlalchemy >= 0.9.9
Requires:      python-webob >= 1.2.3,
Requires:      python-yaql >= 1.0.0
Requires:      MySQL-python
Requires:      %{name}-doc = %{version}-%{release}

%description common
Components common to all OpenStack Murano services

# MURANO-ENGINE
%package engine
Summary: The Murano engine
Group:   Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description engine
OpenStack Murano Engine daemon

# MURANO-API
%package api
Summary: The Murano API
Group:   Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description api
OpenStack rest API to the Murano Engine

# MURANO-CF-API
%package cf-api
Summary: The Murano Cloud Foundry API
Group: System Environment/Base
Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description cf-api
OpenStack rest API for Murano to the Cloud Foundry

%package doc
Summary: Documentation for OpenStack Murano services

%description doc
This package contains documentation files for Murano.

%prep
%setup -q -n murano-%{upstream_version}

%build
%{__python} setup.py build
# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip heat's entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/oslo-config-generator/murano.conf

#%pre
%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# DOCs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
sphinx-build -b man source build/man

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd

mkdir -p %{buildroot}/var/log/murano
mkdir -p %{buildroot}/var/run/murano
mkdir -p %{buildroot}/var/cache/murano
mkdir -p %{buildroot}/etc/murano/
# install systemd unit files
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/murano-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/murano-engine.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/murano-cf-api.service
# install logrotate rules
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/murano
# install default config files
#cd %{_builddir}/murano-%{upstream_version} && oslo-config-generator --config-file ./etc/oslo-config-generator/murano.conf
install -p -D -m 640 %{_builddir}/murano-%{upstream_version}/etc/murano/murano.conf.sample %{buildroot}%{_sysconfdir}/murano/murano.conf
install -p -D -m 640 %{_builddir}/murano-%{upstream_version}/etc/murano/netconfig.yaml.samle %{buildroot}%{_sysconfdir}/murano/netconfig.yaml.samle
install -p -D -m 640 %{_builddir}/murano-%{upstream_version}/etc/murano/murano-paste.ini %{buildroot}%{_sysconfdir}/murano/murano-paste.ini
install -p -D -m 640 %{_builddir}/murano-%{upstream_version}/etc/murano/policy.json %{buildroot}%{_sysconfdir}/murano/policy.json
install -p -D -m 640 %{_builddir}/murano-%{upstream_version}/etc/murano/logging.conf.sample %{buildroot}%{_sysconfdir}/murano/logging.conf

# Copy 'meta' folder(murano meta packages written in muranoPL with execution plan main minimal logic)
cp -r %{_builddir}/murano-%{upstream_version}/meta %{buildroot}/var/cache/murano

%clean
rm -rf %{buildroot}

%files common
%{_mandir}/man1/murano*.1.gz
%doc LICENSE
%{python_sitelib}/murano*
%{_bindir}/murano-manage
%{_bindir}/murano-db-manage
%{_bindir}/murano-test-runner
%dir %attr(0755,murano,root) %{_localstatedir}/log/murano
%dir %attr(0755,murano,root) %{_localstatedir}/run/murano
%dir %attr(0755,murano,root) %{_localstatedir}/cache/murano
%dir %attr(0755,murano,root) %{_sysconfdir}/murano
%config(noreplace) %{_sysconfdir}/logrotate.d/murano
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano.conf
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano-paste.ini
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/netconfig.yaml.samle
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/policy.json
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/logging.conf

%pre common
USERNAME=murano
GROUPNAME=$USERNAME
HOMEDIR=/home/$USERNAME
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin -c "OpenStack Murano Daemons" $USERNAME
exit 0

%files engine
%doc README.rst LICENSE
%{_bindir}/murano-engine
%{_unitdir}/murano-engine.service

%post engine
%systemd_post murano-engine.service

%preun engine
%systemd_preun murano-engine.service

%postun engine
%systemd_postun_with_restart murano-engine.service

%files api
%doc README.rst LICENSE
/var/cache/murano/meta
%{_bindir}/murano-api
%{_unitdir}/murano-api.service

%post api
%systemd_post murano-api.service

%preun api
%systemd_preun murano-api.service

%postun api
%systemd_postun_with_restart murano-api.service

%files cf-api
%doc README.rst LICENSE
%{_bindir}/murano-cfapi
%{_unitdir}/murano-cf-api.service

%post cf-api
%systemd_post murano-cf-api.service

%preun cf-api
%systemd_preun murano-cf-api.service

%postun cf-api
%systemd_postun_with_restart murano-cf-api.service

%files doc
%doc doc/build/html

%changelog
