%global _hardened_build 1
%define repo https://github.com/webmproject/libwebp.git
Name:          libwebp
Version:       0.5.0
Release:       1.%{dist}
Group:         Development/Libraries
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       BSD
Vendor: %{vendor}
Packager: %{packager}
#Source0:       http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
#Source1:       libwebp_jni_example.java
BuildRequires: libjpeg-devel swig libpng-devel giflib-devel libtiff-devel autoconf automake libtool freeglut-devel

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package tools
Group:         Development/Tools
Summary:       The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package devel
Group:         Development/Libraries
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package java
Group:         Development/Libraries
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      java-headless
Requires:      jpackage-utils

%description java
Java bindings for libwebp.

#%prep
#%setup -q

%setup -q -c -T

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
export JAVA_HOME="/usr/java/current/bin"
export PATH=$PATH:$JAVA_HOME
export CPPFLAGS="-I/usr/java/current/include"
autoreconf -vif
./configure --disable-static --enable-libwebpmux \
           --enable-libwebpdemux --enable-libwebpdecoder

make %{?_smp_mflags}

# swig generated Java bindings

#cp %{SOURCE1} .
cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
mkdir -p java/com/google/webp

swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{optflags} -fPIC -shared \
    -I/usr/java/current/include \
    -I/usr/java/current/include/linux \
    -I../src \
    -L../src/.libs -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
/usr/java/current/bin/javac com/google/webp/libwebp.java com/google/webp/libwebpJNI.java
/usr/java/current/bin/jar cvf ../libwebp.jar com/google/webp/*.class

%install
cd %{name}-%{version}
%make_install

# swig generated Java bindings
mkdir -p %{buildroot}/%{_libdir}/%{name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{name}-java/

find %{buildroot} -name "*.la" -exec rm -f {} \;

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files tools
/usr/local/bin/cwebp
/usr/local/bin/dwebp
/usr/local/bin/gif2webp
/usr/local/bin/webpmux
/usr/local/bin/vwebp
/usr/local/share/man*/*

%files -n %{name}
/usr/local/lib//%{name}.so.6*
/usr/local/lib/%{name}decoder.so.2*
/usr/local/lib/%{name}demux.so.2*
/usr/local/lib/%{name}mux.so.2*

%files devel
/usr/local/lib//%{name}*.so
/usr/local/include/*
/usr/local/lib//pkgconfig/*

%files java
#%doc libwebp_jni_example.java
%{_libdir}/%{name}-java/

%changelog
