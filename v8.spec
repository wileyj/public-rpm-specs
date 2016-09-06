%global somajor 3
%global sominor 14
%global sobuild 5
%global sotiny 10
%global sover %{somajor}.%{sominor}.%{sobuild}

Name:		v8
Version:	%{somajor}.%{sominor}.%{sobuild}.%{sotiny}
Release:	25.%{?dist}
Epoch:		1
Summary:	JavaScript Engine
Group:		System Environment/Libraries
License:	BSD
URL:		http://code.google.com/p/v8
Source0:	http://commondatastorage.googleapis.com/chromium-browser-official/v8-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:	%{ix86} x86_64 %{arm}
BuildRequires:	scons, readline-devel, libicu-devel
Provides:	v8-314 = %{version}
Patch1:		v8-3.14.5.8-CVE-2013-2634.patch
Patch2:     v8-3.14.5.10-CVE-2013-2882.patch
Patch3:     v8-3.14.5.10-CVE-2013-6640.patch
Patch4:     v8-3.14.5.10-enumeration.patch
Patch5:     v8-3.14.5.10-CVE-2013-6650.patch
Patch6:     v8-3.14.5.10-CVE-2014-1704-1.patch
Patch7:     v8-3.14.5.10-use-clock_gettime.patch
Patch8:     v8-3.14.5.10-x64-compare-stubs.patch
Patch9:     v8-3.14.5.10-mem-corruption-stack-overflow.patch
Patch10:    v8-3.14.5.10-x64-MathMinMax.patch
Patch11:    v8-3.14.5.10-unused-local-typedefs.patch
Patch12:    v8-3.14.5.10-CVE-2013-6668.patch
Patch13:    v8-3.14.5.10-CVE-2013-6668-segfault.patch
Patch15:    v8-3.14.5.10-abort-uncaught-exception.patch
Patch16:    v8-3.14.5.10-unhandled-ReferenceError.patch
Patch17:    v8-3.14.5.10-busy-loop.patch
Patch18:    v8-3.14.5.10-profiler-log.patch
Patch19:    v8-3.4.14-CVE-2014-3152.patch
Patch20:    v8-3.14.5.10-REPLACE_INVALID_UTF8.patch
Patch21:    v8-3.14.5.10-CVE-2016-1669.patch
Patch22:    v8-3.14.5.10-report-builtins-by-name.patch

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and is used 
in Google Chrome, the open source browser from Google. V8 implements ECMAScript 
as specified in ECMA-262, 3rd edition.

%package devel
Group:		Development/Libraries
Summary:	Development headers and libraries for v8
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:       v8-314-devel = %{version}

%description devel
Development headers and libraries for v8.

%package python
Summary:	Python libraries from v8
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:       v8-314-python = %{version}

%description python
Python libraries from v8.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch15 -p1 -b .abort-uncaught-exception
%patch16 -p1 -b .unhandled-ReferenceError
%patch17 -p1 -b .busy-loop
%patch18 -p1 -b .profiler-log
%patch19 -p1 -b .cve20143152
%patch20 -p1 -b .riu
%patch21 -p1 -b .CVE-2016-1669
%patch22 -p1 -b .builtinname

#Patch7 needs -lrt on glibc < 2.17 (RHEL <= 6)
%if (0%{?rhel} > 6 || 0%{?fedora} > 18)
%global lrt %{nil}
%else
%global lrt -lrt
%endif

# -fno-strict-aliasing is needed with gcc 4.4 to get past some ugly code
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS %{lrt} -fPIC -fno-strict-aliasing -Wno-unused-parameter -Wno-error=strict-overflow -Wno-unused-but-set-variable -fno-delete-null-pointer-checks\'| sed "s/ /',/g" | sed "s/',/', '/g"`
sed -i "s|'-O3',|$PARSED_OPT_FLAGS,|g" SConstruct

# clear spurious executable bits
find . \( -name \*.cc -o -name \*.h -o -name \*.py \) -a -executable \
  |while read FILE ; do
    echo $FILE
    chmod -x $FILE
  done

%build
mkdir -p obj/release/
export GCC_VERSION="44"
scons library=shared snapshots=on \
arch=x64 \
visibility=default \
env=CCFLAGS:"-fPIC" \
I_know_I_should_build_with_GYP=yes

export ICU_LINK_FLAGS=`pkg-config --libs-only-l icu-i18n`

rm -rf libv8.so libv8preparser.so
g++ $RPM_OPT_FLAGS -fPIC -o libv8preparser.so.%{sover} -shared -Wl,-soname,libv8preparser.so.%{somajor} \
	obj/release/allocation.os \
	obj/release/bignum.os \
	obj/release/bignum-dtoa.os \
	obj/release/cached-powers.os \
	obj/release/diy-fp.os \
	obj/release/dtoa.os \
	obj/release/fast-dtoa.os \
	obj/release/fixed-dtoa.os \
	obj/release/preparse-data.os \
	obj/release/preparser-api.os \
	obj/release/preparser.os \
	obj/release/scanner.os \
	obj/release/strtod.os \
	obj/release/token.os \
	obj/release/unicode.os \
	obj/release/utils.os

export RELEASE_BUILD_OBJS=`echo obj/release/*.os | sed 's|obj/release/preparser-api.os||g'`
g++ $RPM_OPT_FLAGS -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} $RELEASE_BUILD_OBJS obj/release/extensions/*.os obj/release/x64/*.os $ICU_LINK_FLAGS
ln -sf libv8.so.%{sover} libv8.so
ln -sf libv8preparser.so.%{sover} libv8preparser.so
scons d8 \
I_know_I_should_build_with_GYP=yes \
arch=x64 \
snapshots=on console=readline visibility=default || :

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -p include/*.h %{buildroot}%{_includedir}
install -p libv8.so.%{sover} %{buildroot}%{_libdir}
install -p libv8preparser.so.%{sover} %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
install -p -m0755 d8 %{buildroot}%{_bindir}

pushd %{buildroot}%{_libdir}
ln -sf libv8.so.%{sover} libv8.so
ln -sf libv8.so.%{sover} libv8.so.%{somajor}
ln -sf libv8.so.%{sover} libv8.so.%{somajor}.%{sominor}
ln -sf libv8preparser.so.%{sover} libv8preparser.so
ln -sf libv8preparser.so.%{sover} libv8preparser.so.%{somajor}
ln -sf libv8preparser.so.%{sover} libv8preparser.so.%{somajor}.%{sominor}
popd
chmod -x %{buildroot}%{_includedir}/v8*.h
mkdir -p %{buildroot}%{_includedir}/v8/extensions/
install -p src/extensions/*.h %{buildroot}%{_includedir}/v8/extensions/
chmod -x %{buildroot}%{_includedir}/v8/extensions/*.h
install -d %{buildroot}%{python_sitelib}
sed -i 's|/usr/bin/python2.4|/usr/bin/env python|g' tools/jsmin.py
sed -i 's|/usr/bin/python2.4|/usr/bin/env python|g' tools/js2c.py
install -p -m0744 tools/jsmin.py %{buildroot}%{python_sitelib}/
install -p -m0744 tools/js2c.py %{buildroot}%{python_sitelib}/
chmod -R -x %{buildroot}%{python_sitelib}/*.py*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}/d8
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%dir %{_includedir}/v8/
%{_includedir}/v8/extensions/
%{_libdir}/*.so

%files python
%{python_sitelib}/j*.py*

%changelog
