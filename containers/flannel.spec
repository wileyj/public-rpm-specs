%define repo https://github.com/coreos/flannel
%define gitversion %(echo `curl -s %{repo}/releases | grep 'span class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1
%define flannel_dir /opt/%{name}

Name:           flannel
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        flannel is a network fabric for containers, designed for Kubernetes 
License:        ASL
Packager:       %{packager}
Vendor:         %{vendor}
URL:            %{repo}
Group:          System Environment/Containers
BuildRequires:  git kernel-headers golang gcc
BuildRequires:  golang-golang-x-net
BuildRequires:  golang-github-coreos-flannel
BuildRequires:  golang-github-coreos-pkg

%description
Sysdig is a universal system visibility tool with native support for containers

%package devel
Group:          System Environment/Base
Summary:        %{name} devel tools
Requires:       %{name} = %{version}-%{release}

%description devel
%{name} devel tools


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}
make dist/flanneld

%install
rm -rf %{buildroot}
cd %{name}-%{version}/build/release
make DESTDIR=%{buildroot} INSTALL="install -p" install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root)

%files devel
%defattr(-, root, root)
