# Hi Googlers! If you're looking in here for patches, nifty.
# You (and everyone else) are welcome to use any of my Chromium spec files and
# patches under the terms of the GPLv2 or later.
# You (and everyone else) are welcome to use any of my V8-specific spec files
# and patches under the terms of the BSD license.
# You (and everyone else) may NOT use my spec files or patches under any other
# terms.
# I hate to be a party-pooper here, but I really don't want to help Google
# make a proprietary browser. There are enough of those already.
# All copyrightable work in these spec files and patches is Copyright 2011
# Tom Callaway <spot@fedoraproject.org>

# For the 1.2 branch, we use 0s here
# For 1.3+, we use the three digit versions
# Hey, now there are four digits. What do they mean? Popsicle.
%global somajor 3
%global sominor 14
%global sobuild 5
%global sotiny 10
%global sover %{somajor}.%{sominor}.%{sobuild}

# %%global svnver 20110721svn8716

Name:		v8
Version:	%{somajor}.%{sominor}.%{sobuild}.%{sotiny}
Release:	22.%{?dist}
Epoch:		1
Summary:	JavaScript Engine
Group:		System Environment/Libraries
License:	BSD
URL:		http://code.google.com/p/v8
Source0:	http://commondatastorage.googleapis.com/chromium-browser-official/v8-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:	%{ix86} x86_64 %{arm}
BuildRequires:	scons, readline-devel, libicu-devel
BuildRequires:	valgrind-devel

#backport fix for CVE-2013-2634 (RHBZ#924495)
Patch1:		v8-3.14.5.8-CVE-2013-2634.patch

#backport fix for CVE-2013-2882 (RHBZ#991116)
Patch2:     v8-3.14.5.10-CVE-2013-2882.patch

#backport fix for CVE-2013-6640 (RHBZ#1039889)
Patch3:     v8-3.14.5.10-CVE-2013-6640.patch

#backport fix for enumeration for objects with lots of properties
#   https://codereview.chromium.org/11362182
Patch4:     v8-3.14.5.10-enumeration.patch

#backport fix for CVE-2013-6640 (RHBZ#1059070)
Patch5:     v8-3.14.5.10-CVE-2013-6650.patch

#backport only applicable fix for CVE-2014-1704 (RHBZ#1077136)
#the other two patches don't affect this version of v8
Patch6:     v8-3.14.5.10-CVE-2014-1704-1.patch

# use clock_gettime() instead of gettimeofday(), which increases performance
# dramatically on virtual machines
# https://github.com/joyent/node/commit/f9ced08de30c37838756e8227bd091f80ad9cafa
# see above link or head of patch for complete rationale
Patch7:     v8-3.14.5.10-use-clock_gettime.patch

# fix corner case in x64 compare stubs
# fixes bug resulting in an incorrect result when comparing certain integers
# (e.g. 2147483647 > -2147483648 is false instead of true)
# https://code.google.com/p/v8/issues/detail?id=2416
# https://github.com/joyent/node/issues/7528
Patch8:     v8-3.14.5.10-x64-compare-stubs.patch

# backport security fix for memory corruption/stack overflow (RHBZ#1125464)
# https://groups.google.com/d/msg/nodejs/-siJEObdp10/2xcqqmTHiEMJ
# https://github.com/joyent/node/commit/530af9cb8e700e7596b3ec812bad123c9fa06356
Patch9:     v8-3.14.5.10-mem-corruption-stack-overflow.patch

# backport bugfix for x64 MathMinMax:
#   Fix x64 MathMinMax for negative untagged int32 arguments.
#   An untagged int32 has zeros in the upper half even if it is negative.
#   Using cmpq to compare such numbers will incorrectly ignore the sign.
# https://github.com/joyent/node/commit/3530fa9cd09f8db8101c4649cab03bcdf760c434
Patch10:    v8-3.14.5.10-x64-MathMinMax.patch

# backport bugfix that eliminates unused-local-typedefs warning
# https://github.com/joyent/node/commit/53b4accb6e5747b156be91a2b90f42607e33a7cc
Patch11:    v8-3.14.5.10-unused-local-typedefs.patch

# backport security fix: Fix Hydrogen bounds check elimination
# resolves CVE-2013-6668 (RHBZ#1086120)
# https://github.com/joyent/node/commit/fd80a31e0697d6317ce8c2d289575399f4e06d21
Patch12:    v8-3.14.5.10-CVE-2013-6668.patch

# backport fix to segfault caused by the above patch
# https://github.com/joyent/node/commit/3122e0eae64c5ab494b29d0a9cadef902d93f1f9
Patch13:    v8-3.14.5.10-CVE-2013-6668-segfault.patch

# Use system valgrind header
# https://bugzilla.redhat.com/show_bug.cgi?id=1141483
Patch14:    v8-3.14.5.10-system-valgrind.patch

# Fix issues with abort on uncaught exception
# https://github.com/joyent/node/pull/8666
# https://github.com/joyent/node/issues/8631
# https://github.com/joyent/node/issues/8630
Patch15:    v8-3.14.5.10-abort-uncaught-exception.patch

# Fix unhandled ReferenceError in debug-debugger.js
# https://github.com/joyent/node/commit/0ff51c6e063e3eea9e4d9ea68edc82d935626fc7
# https://codereview.chromium.org/741683002
Patch16:    v8-3.14.5.10-unhandled-ReferenceError.patch

# Don't busy loop in CPU profiler thread
# https://github.com/joyent/node/pull/8789
Patch17:    v8-3.14.5.10-busy-loop.patch

# Log V8 version in profiler log file
# (needed for compatibility with profiler tools)
# https://github.com/joyent/node/pull/9043
# https://codereview.chromium.org/806143002
Patch18:    v8-3.14.5.10-profiler-log.patch

# Fix CVE in ARM code
# https://bugzilla.redhat.com/show_bug.cgi?id=1101057
# https://codereview.chromium.org/219473002
Patch19:    v8-3.4.14-CVE-2014-3152.patch

# Add REPLACE_INVALID_UTF8 handling that nodejs needs
Patch20:    v8-3.14.5.10-REPLACE_INVALID_UTF8.patch

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and is used 
in Google Chrome, the open source browser from Google. V8 implements ECMAScript 
as specified in ECMA-262, 3rd edition.

%package devel
Group:		Development/Libraries
Summary:	Development headers and libraries for v8
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Development headers and libraries for v8.

%package python
Summary:	Python libraries from v8
Requires:	%{name} = %{epoch}:%{version}-%{release}

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
%patch14 -p1 -b .system-valgrind
%patch15 -p1 -b .abort-uncaught-exception
%patch16 -p1 -b .unhandled-ReferenceError
%patch17 -p1 -b .busy-loop
%patch18 -p1 -b .profiler-log
%patch19 -p1 -b .cve20143152
%patch20 -p1 -b .riu

# Do not need this lying about.
rm -rf src/third_party/valgrind

#Patch7 needs -lrt on glibc < 2.17 (RHEL <= 6)
%if (0%{?rhel} > 6 || 0%{?fedora} > 18)
%global lrt %{nil}
%else
%global lrt -lrt
%endif

# -fno-strict-aliasing is needed with gcc 4.4 to get past some ugly code
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS %{lrt} -fPIC -fno-strict-aliasing -Wno-unused-parameter -Wno-error=strict-overflow -Wno-unused-but-set-variable\'| sed "s/ /',/g" | sed "s/',/', '/g"`
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

# SCons is going away, but for now build with
# I_know_I_should_build_with_GYP=yes
scons library=shared snapshots=on \
%ifarch x86_64
arch=x64 \
%endif
%ifarch armv7hl armv7hnl
armeabi=hard \
%endif
%ifarch armv5tel armv6l armv7l
armeabi=soft \
%endif
visibility=default \
env=CCFLAGS:"-fPIC" \
I_know_I_should_build_with_GYP=yes

%if 0%{?fedora} >= 16
export ICU_LINK_FLAGS=`pkg-config --libs-only-l icu-i18n`
%else
export ICU_LINK_FLAGS=`pkg-config --libs-only-l icu`
%endif

# When will people learn to create versioned shared libraries by default?
# first, lets get rid of the old .so file
rm -rf libv8.so libv8preparser.so
# Now, lets make it right.
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

# "obj/release/preparser-api.os" should not be included in the libv8.so file.
export RELEASE_BUILD_OBJS=`echo obj/release/*.os | sed 's|obj/release/preparser-api.os||g'`

%ifarch %{arm}
g++ $RPM_OPT_FLAGS -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} $RELEASE_BUILD_OBJS obj/release/extensions/*.os obj/release/arm/*.os $ICU_LINK_FLAGS
%endif
%ifarch %{ix86}
g++ $RPM_OPT_FLAGS -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} $RELEASE_BUILD_OBJS obj/release/extensions/*.os obj/release/ia32/*.os $ICU_LINK_FLAGS
%endif
%ifarch x86_64
g++ $RPM_OPT_FLAGS -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} $RELEASE_BUILD_OBJS obj/release/extensions/*.os obj/release/x64/*.os $ICU_LINK_FLAGS
%endif

# We need to do this so d8 can link against it.
ln -sf libv8.so.%{sover} libv8.so
ln -sf libv8preparser.so.%{sover} libv8preparser.so

# This will fail to link d8 because it doesn't use the icu libs.
# Don't build d8 shared. Stupid Google. Hate.
# SCons is going away, but for now build with
# I_know_I_should_build_with_GYP=yes
scons d8 \
I_know_I_should_build_with_GYP=yes \
%ifarch x86_64
arch=x64 \
%endif
%ifarch armv7hl armv7hnl
armeabi=hard \
%endif
%ifarch armv5tel armv6l armv7l
armeabi=soft \
%endif
snapshots=on console=readline visibility=default || :
# library=shared snapshots=on console=readline visibility=default || :

# Sigh. I f*****g hate scons.
# But gyp is worse.
# rm -rf d8

# g++ $RPM_OPT_FLAGS -o d8 obj/release/d8.os -lreadline -lpthread -L. -lv8 $ICU_LINK_FLAGS

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

# install Python JS minifier scripts for nodejs
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
