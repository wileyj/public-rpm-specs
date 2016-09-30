%define repo https://github.com/draios/sysdig
%define gitversion %(echo `curl -s %{repo}/releases | grep 'span class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%define rel_version 1

Name:           sysdig
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        Sysdig is a universal system visibility tool with native support for containers
License:        GPL
Packager:       %{packager}
Vendor:         %{vendor}
URL:            https://sysdig.com
Group:          System Environment/Base
BuildRequires:  git cmake

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
mkdir -p build/release
cd build/release
cmake -DCMAKE_BUILD_TYPE=release -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=ON -DARCHIVE_INSTALL_DIR=%{buildroot} -G "Unix Makefiles" ../..
make

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
/usr/local/bin/c%{name}
/usr/local/bin/%{name}
/usr/local/bin/%{name}-probe-loader
/usr/local/etc/bash_completion.d/%{name}
/usr/local/share/man/man8/c%{name}.*
/usr/local/share/man/man8/%{name}.*

%dir /usr/local/share/%{name}/chisels
/usr/local/share/%{name}/chisels/*
/usr/local/share/zsh/site-functions/_%{name}
/usr/local/share/zsh/vendor-completions/_%{name}

%files devel
%defattr(-, root, root)
/usr/local/src/%{name}*
