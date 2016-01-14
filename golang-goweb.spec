%define srcname goweb

%global provider        github
%global provider_tld    com
%global project         stretchr
%global repo            %{srcname}
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           golang-%{srcname}
Version:        2.0.0
Release:        1.%{dist}
Summary:	A lightweight RESTful web framework for Go.
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
Source0:        golang-%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:	git
BuildRequires:  golang >= 1.2.1-3
BuildRequires:	golang-stew
BuildRequires:	golang-codecs
BuildRequires:	golang-go
BuildRequires:	golang-mgo
Requires:       golang >= 1.2.1-3
Requires:       golang
Requires:       golang-codecs
Requires:       golang-stew
Requires:       golang-mgo

Provides:       golang-%{srcname}
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/webcontext) = %{version}-%{release}
Provides:       golang(%{import_path}/responders) = %{version}-%{release}
Provides:       golang(%{import_path}/handlers) = %{version}-%{release}
Provides:       golang(%{import_path}/paths) = %{version}-%{release}
Provides:       golang(%{import_path}/http) = %{version}-%{release}
Provides:       golang(%{import_path}/controllers) = %{version}-%{release}
Provides:       golang(%{import_path}/context) = %{version}-%{release}

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
cp -pav *.yml %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav context %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav http %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav paths %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav controllers %{buildroot}/%{gopath}/src/%{import_path}/  
cp -rpav handlers %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav responders %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav webcontext %{buildroot}/%{gopath}/src/%{import_path}/

%check
# disabled due to mgo naming mismatch with codecs
GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
