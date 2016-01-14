Name: libtevent
Version: 0.9.21
Release: 1.%{dist}
Group: System Environment/Daemons
Summary: The tevent library
License: LGPLv3+
Vendor: %{vendor}
Packager: %{packager}
URL: http://tevent.samba.org/
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: libtalloc-devel >= 2.0.7
%if 0%{?el6}
BuildRequires: python27-devel
%else
BuildRequires: python-devel
%endif

BuildRequires: pytalloc-devel >= 2.0.7
BuildRequires: doxygen
BuildRequires: docbook-style-xsl
BuildRequires: libxslt

Provides: bundled(libreplace)

%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}
Requires: libtalloc-devel%{?_isa} >= 2.0.7
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tevent library.


%package -n python-tevent
Group: Development/Libraries
Summary: Python bindings for the Tevent library
Requires: libtevent%{?_isa} = %{version}-%{release}

%description -n python-tevent
Python bindings for libtevent

%prep
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
# Taken from specfile for python-simplejson
UpdateTimestamps() {
  Level=$1
  PatchFile=$2

  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}

%setup -q -n tevent-%{version}

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

make %{?_smp_mflags} V=1

doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtevent.a

# Install API docs
rm -f doc/man/man3/todo*
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%{_mandir}/man3/tevent*.gz

%files -n python-tevent
%defattr(-,root,root,-)
%if 0%{?el6}
%{python27_sitearch}/tevent.py*
%{python27_sitearch}/_tevent.so
%else
%{python_sitearch}/tevent.py*
%{python_sitearch}/_tevent.so
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
