%define srcname x2j

%global provider        github
%global provider_tld    com
%global project         clbanning
%global repo            %{srcname}
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           golang-%{srcname}
Version:        0.0.1
Release:        1.%{dist}
Summary:	Unmarshal an anonymous XML doc to map[string]interface{} and JSON, and extract values
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
Requires:       golang >= 1.2.1-3
Requires:       golang
Provides:       golang-%{srcname}
Provides:       golang(%{import_path}) = %{version}-%{release}

%description
%{summary}

This package contains library source intended for 
building other packages which use %{project}/%{repo}.

%prep
%setup -q -n golang-%{srcname}-%{version}

%build
git pull

%install
mv README README.md
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/

%check
GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog