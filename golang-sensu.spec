%global _python_bytecompile_errors_terminate_build 0
%global provider        github
%global provider_tld    com
%global repo_owner      bencaron
%global project         sensu
%global import_path     %{provider}.%{provider_tld}/%{repo_owner}/%{project}
%define _summary        A monitoring framework that aims to be simple, malleable, and scalable. https://sensuapp.org

Name:           golang-%{project}
Version:        1.0.0
Release:        1.%{dist}
Summary:        %{_summary}
License:        MIT
Vendor:         %{vendor}
Packager:       %{packager}
BuildArch:      noarch
BuildRequires:  git golang >= 1.5.0 golang-objx golang-testify
Requires:       golang >= 1.5.0 golang-testify golang-objx golang-logger golang-httpauth uchiwa-web uchiwa
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang-%{provider}

%description
%{summary}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone https://github.com/%{repo_owner}/%{project}.git %{name}-%{version}

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/

%check
#GOPATH=%{buildroot}/%{gopath}:%{gopath} go test %{import_path}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}

%changelog
