Summary: Gives a fake chroot environment
Name: fakechroot
Version: 2.9
Release: 23.%{dist}
License: LGPLv2+
Vendor: %{vendor}
Packager: %{packager}
Group: Development/Tools
URL: http://fakechroot.alioth.debian.org/
Source0: http://ftp.debian.org/debian/pool/main/f/fakechroot/%{name}_%{version}.orig.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: fakechroot-libs = %{version}-%{release}

# Required for patch0:
BuildRequires: autoconf, automake, libtool

# Fix build problems with recent glibc.  Sent upstream 20090414.
Patch0: fakechroot-scandir.patch

# Add FAKECHROOT_CMD_SUBST feature.
# Sent upstream 20090413.  Accepted upstream 20090418.
Patch1: fakechroot-cmd-subst.patch

# Patch to version of aclocal/automake.
Patch2: fakechroot-autogen.patch

%description
fakechroot runs a command in an environment were is additionally
possible to use the chroot(8) call without root privileges. This is
useful for allowing users to create their own chrooted environment
with possibility to install another packages without need for root
privileges.

%package libs
Summary: Gives a fake chroot environment (libraries)
Group: Development/Tools

%description libs
This package contains the libraries required by %{name}.

%prep
%setup -q

%patch0 -p0
%patch1 -p0
%patch2 -p1

# Patch0 updates autoconf, so rerun this:
./autogen.sh

%build
%configure \
  --disable-dependency-tracking \
  --disable-static
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%check
#make check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%doc LICENSE scripts/ldd.fake scripts/restoremode.sh scripts/savemode.sh
%{_bindir}/fakechroot
%{_mandir}/man1/fakechroot.1.gz

%files libs
%dir %{_libdir}/fakechroot
%exclude %{_libdir}/fakechroot/libfakechroot.la
%{_libdir}/fakechroot/libfakechroot.so

%changelog
