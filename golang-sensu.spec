%define srcname sensu

%global provider        github
%global provider_tld    com
%global project         bencaron
%global repo            gosensu
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           golang-%{srcname}
Version:        0.0.1
Release:        1.%{dist}
Summary:        Gosensu is an golang wrapper around the Sensu API
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
Source0:        golang-%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  git golang
BuildRequires:  golang-objx
BuildRequires:  golang-testify
Requires:       golang
Requires: 	golang-testify
Requires: 	golang-objx
Requires: 	golang-logger
Requires: 	golang-httpauth
Requires: 	uchiwa-web uchiwa
Provides:       golang-%{srcname}

%description
%{summary}

This package contains library source intended for 
building other packages which use %{project}/%{repo}.

%prep
%setup -q -n golang-%{srcname}-%{version}

%build
git pull

%install
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/

%check
# Disabled due to requiring working networking
# export SENSU_SERVER_URL="http://hidden-ravine-4272.herokuapp.com"
# GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files 
%doc README.md LICENSE
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog


