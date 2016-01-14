%define srcname codecs

%global provider        github
%global provider_tld    com
%global project         stretchr
%global repo            %{srcname}
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           golang-%{srcname}
Version:        0.0.1
Release:        1.%{dist}
Summary:	A lightweight RESTful web framework for Go.
License:        MIT
Vendor: %{vendor}
Packager: %{packager}
Source0:        golang-%{srcname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:	git
BuildRequires:  golang >= 1.2.1-3
Requires:       golang >= 1.2.1-3
Requires:       golang
Provides:       golang-%{srcname}
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/bson) = %{version}-%{release}
Provides:       golang(%{import_path}/constants) = %{version}-%{release}
Provides:       golang(%{import_path}/csv) = %{version}-%{release}
Provides:       golang(%{import_path}/json) = %{version}-%{release}
Provides:       golang(%{import_path}/jsonp) = %{version}-%{release}
Provides:       golang(%{import_path}/msgpack) = %{version}-%{release}
Provides:       golang(%{import_path}/services) = %{version}-%{release}
Provides:       golang(%{import_path}/test) = %{version}-%{release}
Provides:       golang(%{import_path}/xml) = %{version}-%{release}

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
cp -rpav bson %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav constants %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav csv %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav json %{buildroot}/%{gopath}/src/%{import_path}/  
cp -rpav jsonp %{buildroot}/%{gopath}/src/%{import_path}/  
cp -rpav msgpack %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav services %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav test %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav xml %{buildroot}/%{gopath}/src/%{import_path}/


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
