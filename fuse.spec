Name:           fuse
Version:        2.9.4
Release:        1.%{?dist}
Summary:        File System in Userspace (FUSE) utilities

Group:          System Environment/Base
License:        GPL+
URL:            http://fuse.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.conf

Patch1:         fuse-0001-More-parentheses.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=970768
Patch2:         fuse-2.9.2-namespace-conflict-fix.patch
# Allow setting SELinux context on fuse mounts: backport from master
# c52cafc81ced83fbd5cc7edf4ef5f7cb57b82729 , with ChangeLog changes
# dropped as they conflict
Patch3:         0001-libfuse-pass-security-context-options-to-kernel.patch
Requires:       which
Conflicts:      filesystem < 3
BuildRequires:  libselinux-devel

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
Group:          System Environment/Libraries
License:        LGPLv2+
Conflicts:      filesystem < 3

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+
Conflicts:      filesystem < 3

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
%patch1 -p1 -b .add_parentheses
%patch2 -p1 -b .conflictfix
%patch3 -p1 -b .context

%build
# Can't pass --disable-static here, or else the utils don't build
export MOUNT_FUSE_PATH="%{_sbindir}"
CFLAGS="%{optflags} -D_GNU_SOURCE" %configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a
# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse

# Install config-file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

# Delete pointless udev rules, which do not belong in /etc (brc#748204)
rm -f %{buildroot}%{_sysconfdir}/udev/rules.d/99-fuse.rules

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
%{_sbindir}/mount.fuse
%attr(4755,root,root) %{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%doc COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files devel
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
