%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            go-etcd
%global commit          6fe04d580dfb71c9e34cbce2f4df9eefd1e1241e

%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global debug_package   %{nil}

Name:       golang-%{provider}-%{project}-%{repo}
Version:    0.2.0
Release:    0.4.rc1.git%{shortcommit}%{?dist}
Summary:    The official etcd v0.2 client library for Go
License:    ASL 2.0
URL:        http://%{import_path}
Source0:    https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildArch:      noarch
%else
ExclusiveArch:  %{ix86} x86_64 %{arm}
%endif

%description
%{summary}

%package devel
BuildRequires:  golang >= 1.2.1-3
Requires:       golang >= 1.2.1-3
Summary:        A golang library for logging to systemd
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/etcd) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for building other packages
which use coreos/go-etcd.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/etcd
cp -pav etcd/*.go  %{buildroot}/%{gopath}/src/%{import_path}/etcd

%files devel
%doc LICENSE README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/etcd
%attr(644,-,-) %{gopath}/src/%{import_path}/etcd/*.go

%changelog
* Thu Oct 23 2014 jchaloup <jchaloup@redhat.com> - 0.2.0-0.4.rc1.git6fe04d5
- Choose the correct architecture
  related: #1141807

* Thu Oct 23 2014 jchaloup <jchaloup@redhat.com> - 0.2.0-0.3.rc1.git6fe04d5
- Bump to upstream 6fe04d580dfb71c9e34cbce2f4df9eefd1e1241e
  resolves: #1141807

* Mon Sep 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.2.0-0.2.rc1.git23142f6
 - do not redefine gopath
 - do not own dirs owned by golang
 - correct version number, rc tag goes in release
 - noarch

* Sat Sep 06 2014 Eric Paris <eparis@redhat.com - 0.2.rc1-0.1.git23142f67.2
- Bump to upstream 23142f6773a676cc2cae8dd0cb90b2ea761c853f

* Wed Aug 20 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.2.0-0.1-rc1
- Initial fedora package
