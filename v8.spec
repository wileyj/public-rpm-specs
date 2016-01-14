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

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "import distutils.sysconfig as d; print d.get_python_lib()")}

Name:		v8
Version:	%{somajor}.%{sominor}.%{sobuild}.%{sotiny}
Release:	23.%{dist}
Epoch:		1
Summary:	JavaScript Engine
Group:		System Environment/Libraries
License:	BSD
Packager: %{packager}
Vendor: %{vendor}
URL:		http://code.google.com/p/v8
Source0:	http://commondatastorage.googleapis.com/chromium-browser-official/v8-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:	%{ix86} x86_64 %{arm}
BuildRequires:	scons,readline-devel, libicu-devel, ncurses-devel

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

%prep
%setup -q -n %{name}-%{version}

# -fno-strict-aliasing is needed with gcc 4.4 to get past some ugly code
%if 0%{?el5}
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing -Wno-unused-parameter -lncurses\'| sed "s/ /',/g" | sed "s/',/', '/g"`
sed -i "s|'-O3',|$PARSED_OPT_FLAGS,|g" SConstruct
%else
PARSED_OPT_FLAGS=`echo \'$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing -Wno-unused-parameter \'| sed "s/ /',/g" | sed "s/',/', '/g"`
sed -i "s|'-O3',|$PARSED_OPT_FLAGS,|g" SConstruct
%endif

# clear spurious executable bits
find . \( -name \*.cc -o -name \*.h -o -name \*.py \) -a -executable \
  |while read FILE ; do
    echo $FILE
    chmod -x $FILE
  done

%build
mkdir -p obj/release/
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export GCC_VERSION="48"
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
env=CCFLAGS:"-fPIC"

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
scons d8 \
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
#install -p -m0755 d8 %{buildroot}%{_bindir}


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
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE
#%{_bindir}/d8
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_includedir}/v8/extensions/
%{_libdir}/*.so
%{python_sitelib}/j*.py*


