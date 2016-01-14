%global  VERSION      6.7.7
%global  MVERSION     6.8.8
%global  MPATCH	      10
%define _installpath /opt/JMagick-%{VERSION}
%define _imagemagick /opt/ImageMagick-%{MVERSION}
%define _bindir %{_installpath}/bin
%define _sbindir %{_installpath}/sbin
%define _libexecdir %{_installpath}/libexec
%define _libdir  %{_installpath}/lib
%define _datadir  %{_installpath}/share
%define _includedir  %{_installpath}/include
%define pkgconfig  %{_imagemagick}/lib/pkgconfig


Summary: Jmagick - Java interface to ImageMagick 
Name: jmagick
Version: %{VERSION}
Release: 5.%{dist}
License: LGPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Graphic
Source: jmagick-%{version}.tar.gz
BuildRequires:  libopenjpeg-devel
BuildRequires: ImageMagick-devel = %{MVERSION}.%{MPATCH}, ImageMagick =  %{MVERSION}.%{MPATCH}, jdk, pkgconfig
BuildRequires: freetype-devel, libtiff-devel, libtiff, zlib-devel, libgomp, bzip2-libs, bzip2-devel
Requires: ImageMagick = %{MVERSION}.%{MPATCH}, jdk, libtiff-devel, libtiff
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
JMagick is an open source Java interface of ImageMagick. It is implemented in the form of a thin Java Native Interface (JNI) layer into the ImageMagick API.

%prep
rm -rf %{buildroot}

%setup -n %{name}
G=`ls /usr/java/ | sort -r | grep -m 1 jdk`
export JAVA_HOME="/usr/java/${G}"
export PATH=$PATH:$JAVA_HOME/bin:%{_imagemagick}/bin
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{pkgconfig}

sed -i "s|jar cvf|$JAVA_HOME/bin/jar cvf|g" Makefile
export CPPFLAGS="-I%{_imagemagick}/include"
export LDFLAGS="-L%{_imagemagick}/lib"


./configure --prefix=%{_installpath} \
      --with-magick-home=%{_imagemagick} \
      --with-java-home="$JAVA_HOME" \
      PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{pkgconfig}
%build
mkdir -p $RPM_BUILD_ROOT/%{_installpath}

%{__make} all
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%post
ln -sf %{_installpath}/lib/libJMagick-%{version}.so %{_installpath}/lib/libJMagick.so
ln -sf %{_installpath}/lib/jmagick-%{version}.jar %{_installpath}/lib/jmagick.jar

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{_installpath}


%changelog
