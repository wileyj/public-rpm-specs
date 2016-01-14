%define srcname testify

%global provider        github
%global provider_tld    com
%global project         stretchr
%global repo            %{srcname}
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           golang-%{srcname}
Version:        0.0.1
Release:        1.%{dist}
Summary:        Go code (golang) set of packages that provide many tools for testifying that your code will behave as you intend
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
Provides:       golang(%{import_path}/assert) = %{version}-%{release}
Provides:       golang(%{import_path}/http) = %{version}-%{release}
Provides:       golang(%{import_path}/mock) = %{version}-%{release}
Provides:       golang(%{import_path}/require) = %{version}-%{release}
Provides:       golang(%{import_path}/suite) = %{version}-%{release}

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
cp -rpav require %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav suite %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav http %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav assert %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav mock %{buildroot}/%{gopath}/src/%{import_path}/

#%check
#GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
