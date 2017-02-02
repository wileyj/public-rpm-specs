%define repo https://github.com/zeromq/czmq
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Name:           czmq
Version:        %{gitversion}
Release:        %{rel_version}.%{?dist}
Summary:        the high-level c binding for 0mq

Group:          System Environment/Libraries
License:        MPLv2
URL:            %{repo}

BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xmlto
BuildRequires:  zeromq-devel
BuildRequires:  libuuid-devel
BuildRequires:  systemd-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
czmq the high-level c binding for 0mq.

%package -n libczmq4
Group:          System/Libraries
Summary:        the high-level c binding for 0mq shared library

%description -n libczmq4
This package contains shared library for czmq: the high-level c binding for 0mq

%package devel
Summary:        the high-level c binding for 0mq
Group:          System/Libraries
Requires:       libczmq4 = %{version}
Requires:       zeromq-devel
Requires:       libuuid-devel
Requires:       systemd-devel

%description devel
the high-level c binding for 0mq development tools
This package contains development files for czmq: the high-level c binding for 0mq



%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update
sh autogen.sh
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" configure
%global openpgm_pc $(basename %{_libdir}/pkgconfig/openpgm*.pc .pc)
sed -i "s/openpgm-[0-9].[0-9]/%{openpgm_pc}/g" configure*

%build
cd %{name}-%{version}
autoreconf -fi
%configure 
make -j2 %{?_smp_mflags}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"


# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%post -n libczmq4 -p /sbin/ldconfig
%postun -n libczmq4 -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/zmakecert
%{_mandir}/man1/zmakecert*

%files -n libczmq4
%defattr(-,root,root)
%{_libdir}/libczmq.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libczmq.so
%{_libdir}/pkgconfig/libczmq.pc
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_datadir}/zproject/
%{_datadir}/zproject/czmq/


