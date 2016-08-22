Summary:        Google C++ testing framework
Name:           gtest
Version:        1.6.0
Release:        6.%{dist}
License:        BSD
Vendor: %{vendor}
Packager: %{packager}
Group:          Development/Tools
URL:            http://code.google.com/p/googletest/
Source0:        http://googletest.googlecode.com/files/gtest-%{version}.zip
Patch0:         gtest-soname.patch
BuildRequires:  python27 cmake libtool
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Google's framework for writing C++ tests on a variety of platforms
(GNU/Linux, Mac OS X, Windows, Windows CE, and Symbian). Based on the
xUnit architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       automake
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%setup -q
%patch0 -p1 -b .0-soname

# keep a clean copy of samples.
cp -pr ./samples ./samples.orig

%build
# this is odd but needed only to generate gtest-config.
%configure
mkdir build
pushd build
%cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_SKIP_BUILD_RPATH=TRUE -DPYTHON_EXECUTABLE=%{__python} -Dgtest_build_tests=ON ..
popd

make %{?_smp_mflags} -C build

%install
rm -rf $RPM_BUILD_ROOT
# make install doesn't work anymore.
# need to install them manually.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/aclocal,%{_includedir}/gtest{,/internal},%{_libdir}}
# just for backward compatibility
install -p -m 0755 build/libgtest.so.*.* build/libgtest_main.so.*.* $RPM_BUILD_ROOT%{_libdir}/
(cd $RPM_BUILD_ROOT%{_libdir};
ln -sf libgtest.so.*.* $RPM_BUILD_ROOT%{_libdir}/libgtest.so
ln -sf libgtest_main.so.*.* $RPM_BUILD_ROOT%{_libdir}/libgtest_main.so
)
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
install -p -m 0755 scripts/gtest-config $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 include/gtest/*.h $RPM_BUILD_ROOT%{_includedir}/gtest/
install -p -m 0644 include/gtest/internal/*.h $RPM_BUILD_ROOT%{_includedir}/gtest/internal/
install -p -m 0644 m4/gtest.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc CHANGES CONTRIBUTORS COPYING README
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files devel
%defattr(-, root, root, -)
%doc samples
%{_bindir}/gtest-config
%{_datadir}/aclocal/gtest.m4
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_includedir}/gtest

%changelog
