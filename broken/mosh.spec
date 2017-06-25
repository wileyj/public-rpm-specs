%define prefix /opt/mosh

Name:		mosh
Version:	1.2.5
Release:	1.%{dist}
Summary:	Mobile shell that supports roaming and intelligent local echo
License:	GPLv3+
Vendor: %{vendor}
Packager: %{packager}
Group:		Applications/Internet
URL:		http://mosh.mit.edu/
BuildArch:	x86_64
Source0:	%{name}.tar.gz

BuildRequires:	protobuf-devel
BuildRequires:	libutempter-devel
BuildRequires:	boost-devel
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
Requires:	openssh-clients
Requires:	perl-IO-Tty
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Mosh is a remote terminal application that supports:
  - intermittent network connectivity,
  - roaming to different IP address without dropping the connection, and
  - intelligent local echo and line editing to reduce the effects
    of "network lag" on high-latency connections.

%prep

%setup -q -n %{name}

%build
git pull 
./autogen.sh
./configure --prefix=%{prefix} --with-utempter --enable-completion --enable-server --enable-client --enable-hardening

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_prefix} %{buildroot}%{_mandir}
make install DESTDIR=%{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%doc README.md COPYING ChangeLog
%{prefix}/bin/*
%{prefix}/share/man/man1/*
%{prefix}/etc/*

%changelog
